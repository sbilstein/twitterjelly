# basics
import os
import json
import time

# urllib
import urllib.request
import urllib.parse
import urllib.error

# local libraries
import debuglog
from dbsql import SQLQuery
from tweetadder import TweetAdder
from dammit import UnicodeDammit
from util import *

class TweetFetcher:

    #@perftest
    def __init__(self, sql_obj=None):
        self.rate_data = self.fetchRateData()
        if not sql_obj:
            self.sql = SQLQuery()
        else:
            self.sql = sql_obj

        self.tweet_adder = TweetAdder(sql_obj=self.sql)

    ##@perftest
    def fetchRateData(self):
        return json.loads(urllib.request.urlopen("https://api.twitter.com/1/account/rate_limit_status.json").read().decode("ascii"))

    def checkRateLimit(self):
        debuglog.pprint_msg(self.rate_data)
        debuglog.msg("REMAINING HITS:",self.rate_data['remaining_hits'])
        if time.time() > self.rate_data['reset_time_in_seconds']:
            self.rate_data = self.fetchRateData()

        if "error" in self.rate_data:
            return 60*60
            
        if self.rate_data['remaining_hits'] <= 1:
            debuglog.msg("rate limit: wait",self.rate_data['reset_time_in_seconds'] - time.time() )
            return self.rate_data['reset_time_in_seconds'] - time.time()
        else:
            return 0
    
    def fetchTopUserTweets(self, start_at=None):
        debuglog.msg("Fetching all celebrity tweets...")

        q = "SELECT DISTINCT user FROM celebs"
        results = SQLQuery().q(q)
        users = [result[0] for result in results]
        
        if start_at:
            users = users[users.index(start_at):]
            
        for user in users:
            if self.fetchUserTweets(user):
                 debuglog.msg("\tSuccessfully fetched tweets for @%s :)"%user)
            else:
                 debuglog.msg("\tFailed to fetch tweets for @%s :("%user)
            time.sleep(1)

    def fetchUserTweets(self, user):
        """
        Fetch tweets for user and add to the database.
        """
        data = self.getUserTweetsData(user)
        for tweet in data['results']:
            if self.tweet_adder.add(tweet):
               debuglog.msg("successfully added")
            else:
               debuglog.msg("failed to add :(")
        return True

    def getUserTweetsData(self,user):        
        debuglog.msg("=====\n\nGetting data for @%s from Search API..."%user)
        try:
            twitter_query = "from:%s"%user
            twitter_query = urllib.parse.quote(twitter_query)

            query_url = "http://search.twitter.com/search.json?lang=en&rpp=100&q=%s"%twitter_query

            response_unicode = UnicodeDammit(urllib.request.urlopen(query_url).read())
            data = json.loads(response_unicode.unicode_markup,
                encoding=response_unicode.original_encoding if response_unicode.original_encoding else "utf-8")
            debuglog.msg("\tGot %s tweets for @%s from Search API."%(str(len(data['results'])), user))
            return data
        except:
            debuglog.msg("\tFailed to get data from Search API :(")
            debuglog.msg("\t\tURL:\t%s"%query_url)
            return { 'results': [] }

    def fetchTopUserTimelines(self):
        top_users = open('update_users.txt','r').readlines()
        top_users = [user.replace('\n','') for user in top_users]

        for user in top_users:
            debuglog.msg("Getting timeline for",user)
            status='retry'
            while status == 'retry' or status=='wait':
                debuglog.msg(status)
                debuglog.msg("\tFetching timeline for @%s in %s seconds..."%(user, str(self.checkRateLimit())))
                status = self.fetchUserTimeline(user)['status']
                time.sleep(1)
                time.sleep(self.checkRateLimit())
                
            if status == 'success':
                debuglog.msg("\tGot timeline for %s :)"%user)
            elif status == '404':
                debuglog.msg("\tUser not found.")
            else:
                debuglog.msg("\tUnknown error prevented getting user timeline.")

    def canFetchTimeline(self):
        return self.checkRateLimit() <= 0         
        
    def fetchUserTimeline(self, user, format="default", use_cache=True, write_cache=True, use_filesystem_cache=False):
        # TODO: Clean this function up, format parameter does magic it shouldn't be doing.
        # Currently, format="default" means that we're adding celebrity timeline tweets, we never call this.
        # If we do call with format="default" we want to add the timeline tweets to the celebrity tweets table.
        # This is called from DataGrabber to get user timelines with format="searchapi". In this case we want to check
        # if we have matching non-celebrity tweets, and if so return them (in future: possibly add new tweets from
        # search api as well). If not, get tweets from the timeline api, store them in the tweets_non_celeb table,
        # and return an object with those tweets.
        # Also, if a user is cached and called with default, we will just get back the cached data and not insert anything.

        debuglog.msg("Fetching timeline for @%s..."%user)
        got_cache_data = False
        json_txt = "{}"
        json_encoding = "utf-8"

        if use_cache and not use_filesystem_cache:
            q = "SELECT * FROM tweets_non_celeb WHERE from_user=%(user)s;"
            vals = { 'user': user }
            cached_tweets = self.sql.q(q, vals)
            if len(cached_tweets) > 0:
                return [tweet[0] for tweet in cached_tweets]
        elif use_cache and use_filesystem_cache:
            debuglog.msg("\tchecking cache...")
            cached_list = os.listdir('./timelines')
            userjsonfilename = user.lower()+'.json'
            if userjsonfilename in cached_list:
                #modtime = os.stat('./timelines/'+userjsonfilename)[ST_MTIME]
                ##cache stays fresh for a day
                #if ((float(time.time()) - modtime)/60)/60 <= 24:
                debuglog.msg("\t\tgot cache data.")
                json_txt = open('./timelines/'+userjsonfilename,'r').read()
                got_cache_data = True

        if not got_cache_data:
            debuglog.msg("\tNo cache data, calling timeline api...")
            if self.checkRateLimit() > 0:
                debuglog.msg("\t\tHave to wait.")
                return {'status':'wait'}
            url = "https://api.twitter.com/1/statuses/user_timeline.json?&screen_name=%s&count=150"%user
            debuglog.msg(url)
            try:
                response = urllib.request.urlopen(url)
                debuglog.msg(response.info())
            except urllib.error.HTTPError as e:
                if "404" in str(e):
                    return {'status':'404'}
                elif "502" in str(e):
                    return {'status':'retry'}
                else:
                    return {'status':'error'}

            json_unicode = UnicodeDammit(response.read())
            json_txt = json_unicode.unicode_markup
            if json_unicode.original_encoding:
                json_encoding = json_unicode.original_encoding

            if write_cache and use_filesystem_cache:
                fname = './timelines/'+user.lower()+'.json'
                with open(fname,'wt') as f:
                    os.chmod(fname, 0o777)
                    f.write(json_txt)
            
        data = json.loads(json_txt, encoding=json_encoding)
        debuglog.msg("\tdata is...",str(data)[:100])

        if format == "searchapi":
            # For now, format="searchapi" indicates we are getting non-celebrity tweets.
            debuglog.msg("\tGot %d results for %s from user timeline API."%(len(data),user))

            if write_cache and not use_filesystem_cache:
                for non_celeb_timeline_tweet in data:
                    self.tweet_adder.addNonCelebTimelineTweet(non_celeb_timeline_tweet)

            return { 'results':data }

        # For now, format="default" (only way to reach here) means we are adding celebrity tweets.
        for timeline_tweet in data:
            self.tweet_adder.addTimelineTweet(timeline_tweet)
            
        return {'status':'success'}

    def addCeleb(self, celeb):
        print("Adding",celeb)
        q = "INSERT INTO celebs (user) VALUES(%(celeb)s)"
        vals = {'celeb':celeb}

        self.sql.q(q, vals)

        self.fetchUserTimeline(celeb, use_cache=False)

        print("Added",celeb)


if __name__ == '__main__':
    TweetFetcher().fetchTopUserTweets()
    #TweetFetcher().fetchUserTweets("king32david")
    #TweetFetcher().fetchUserTimeline("eminem")
    #TweetFetcher().fetchUserTimeline("ladygaga")
    #TweetFetcher().fetchTopUserTimelines()
    #TweetFetcher().addCeleb("donttrythis")
    #TweetFetcher().addCeleb("AudrinaPatridge")

