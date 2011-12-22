import pickle
import time
import urllib.request
import urllib.parse
import urllib.error
import json
import pprint
import random
from tweetadder import TweetAdder
import os, sys
from stat import *
from dbsql import SQLQuery

class TweetFetcher:   
    def __init__(self):
        """{"reset_time_in_seconds":1323753236,"reset_time":"Tue Dec 13 05:13:56 +0000 2011","hourly_limit":150,"remaining_hits":143}"""
        self.ratedata = self.fetchRateData()
        self.tweetAdder = TweetAdder()

    def fetchRateData(self):
        return json.loads(urllib.request.urlopen("https://api.twitter.com/1/account/rate_limit_status.json").read().decode("ascii"))

    def checkRateLimit(self):
        pprint.pprint(self.ratedata)
        print("REMAINING HITS:",self.ratedata['remaining_hits'])
        if time.time() > self.ratedata['reset_time_in_seconds']:
            self.ratedata = self.fetchRateData()

        if "error" in self.ratedata:
            return 60*60
            
        if self.ratedata['remaining_hits'] <= 1:
            print("rate limit: wait",self.ratedata['reset_time_in_seconds'] - time.time() )
            return self.ratedata['reset_time_in_seconds'] - time.time() 
        else:
            return 0
    
    def fetchTopUserTweets(self, startat=None):
        print("fetching top tweets")
    
        #users = pickle.load(open("topusers.pkl","rb"))
        #users.sort(key=lambda x:random.random())
        q = "SELECT user FROM celebs"
        results = SQLQuery().q(q)
        users = [result[0] for result in results]
        
        if startat:
            users = users[users.index(startat):]
            
        for user in users:
            if self.fetchUserTweets(user):
                print("Successfully fetched tweets for @%s :)"%user)
            else:
                print("Failed to fetch tweets for @%s :("%user)
            time.sleep(1)

    def fetchUserTweets(self, user):
        '''fetch and add to database'''
        data = self.getUserTweetsData(user)
        #pprint.pprint(data)
        for tweet in data['results']:
            if self.tweetAdder.add(tweet):
                print("successfully added")
            else:
                print("failed to add :(")
        return True

    def getUserTweetsData(self,user):        
        print("=====\n\ngetting data for @%s from Search API"%user)
        twitterquery = "from:%s"%user
        twitterquery = urllib.parse.quote(twitterquery)
        print(twitterquery)
        queryurl = "http://search.twitter.com/search.json?lang=en&rpp=100&q=%s"%twitterquery
        print(queryurl)
        data = json.loads(urllib.request.urlopen(queryurl).read().decode("ascii"))
        print("Get %s tweets for @%s from Search API."%(str(len(data['results'])), user))
        return data

    def fetchTopUserTimelines(self):
        #topusers = open('celebs.txt','r').readlines()
        topusers = open('update_users.txt','r').readlines()
        topusers = [user.replace('\n','') for user in topusers]

        for user in topusers:
            print("Getting timeline for",user)
            status='retry';
            while status == 'retry' or status=='wait':
                print(status)
                "Fetching timeline for @%s in %s seconds..."%(user, str(self.checkRateLimit()))
                status = self.fetchUserTimeline(user)['status']
                time.sleep(1)
                time.sleep(self.checkRateLimit())
                
            if status == 'success':
                print("Got timeline for %s :)"%user)
            elif status == '404':
                print("User not found.")
            else:
                print("Unknown error prevented getting user timeline.")

    def canFetchTimeline(self):
        return self.checkRateLimit() <= 0         
        
    def fetchUserTimeline(self, user, usecache=True, writecache=True, format="default"):
        print("fetching time line for",user)
        gotcachedata = False
        json_txt = "{}"
        
        if usecache:
            print("checking cache...")
            cachedlist = os.listdir('./timelines')
            #print(cachedlist)
            userjsonfilename = user.lower()+'.json'
            if userjsonfilename in cachedlist:
                #modtime = os.stat('./timelines/'+userjsonfilename)[ST_MTIME]
                ##cache stays fresh for a day
                #if ((float(time.time()) - modtime)/60)/60 <= 24:
                print("got cache data.")
                json_txt = open('./timelines/'+userjsonfilename,'r').read()
                gotcachedata = True

        if not gotcachedata:
            print("no cache data, calling api...")
            if self.checkRateLimit() > 0:
                print("have to wait")
                return {'status':'wait'}
            url = "https://api.twitter.com/1/statuses/user_timeline.json?&screen_name=%s&count=200"%user
            print(url)
            try:
                response = urllib.request.urlopen(url)
                print(response.info())
            except urllib.error.HTTPError as e:
                if "404" in str(e):
                    return {'status':'404'}
                elif "502" in str(e):
                    return {'status':'retry'}
                else:
                    return {'status':'error'}
                    
            json_txt = response.read().decode("ascii")
            if writecache:
                open('./timelines/'+user.lower()+'.json','w').write(json_txt)
            
        data = json.loads(json_txt)
        print("data is...",str(data)[:100])
        if format == "searchapi":
            print("got %d results for %s from user timeline api"%(len(data),user))
            return {'results':data}
        for timelinetweet in data:
            self.tweetAdder.addTimelineTweet(timelinetweet)
            
        return {'status':'success'}

if __name__ == '__main__':
    TweetFetcher().fetchTopUserTweets()
    #TweetFetcher().fetchUserTweets("king32david")
    #TweetFetcher().fetchUserTimeline("eminem")
    #TweetFetcher().fetchUserTimeline("ladygaga")
    #TweetFetcher().fetchTopUserTimelines()
