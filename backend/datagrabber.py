from dbsql import *
import pprint
from tfidf import *
import time
import math
import pickle
import unidecode
import urllib.request
import json
from doshit import * #random funtions, forgot what they do.
import hashlib
from fetchtweets import TweetFetcher
import tweetadder
import datetime
import collections
import celebmatcher

class DataGrabber:
    def __init__(self):
        self.sql = SQLQuery()
        self.tf = TweetFetcher()

    def GetTweetsForUser(self, username):
        q = "SELECT (text) FROM tweets WHERE from_user=%s"
        v = username
        results = self.sql.q(q,v)
        return results

    def GetTopUsers(self):
        return pickle.load(open('topusers.pkl','rb'))
        
    def GetAllText(self):
        q = "SELECT text FROM tweets"
        return self.sql.q(q)

    def GenerateLDAData(self):
        '''Output tab-separated file to be consumed by LDA.'''
        f = open('ldadata.tsv','w')
        q = "SELECT id, text FROM tweets"
        data = self.sql.q(q)
        
        for d in data:
            try:
                f.write("%s\t%s\n"%(str(d[0]), str(d[1])))
            except UnicodeEncodeError:
                try:
                    f.write("%s\t%s\n"%(str(d[0]).encode("latin1"), str(d[1]).encode("latin1")))
                except:
                    try:
                        f.write("%s\t%s\n"%(unidecode.unidecode(d[0]), unidecode.unidecode(d[1])))
                    except:
                        print("One tough cookie! Couldn't decode this:",d)

        f.close()
        print('done writing LDA data to file!')

    def GetUserTweets(self,user,canretry=True):
        userdata = None
        if self.tf.canFetchTimeline():
            userdata = self.tf.fetchUserTimeline(user, format="searchapi")
        else:
            userdata = self.tf.getUserTweetsData(user)

        if 'results' not in userdata:
            if canretry:
                return self.GetUserTweets(user, canretry=False)
            else:
                userdata = self.tf.getUserTweetsData(user)

        return userdata

    def GetUserTweetStats(self, userdata):

        #declare all counts
        num_days = 0.0

        num_per_time = [0.0]*6

        num_per_weekday = [0.0]*7
        num_at = 0.0
        num_rt = 0.0
        num_hash = 0.0
        num_links = 0.0

        mentions = []
        hashes = []

        user_name = ""
        #tweets per day logic depends on results coming back in chronological order
        #MAKE SURE THIS IS ALWAYS THE CASE IN SEARCH API, REST API, CACHE
        #IF NOT, NEED TO SORT AS PRE PROCESSING STEP
        #JON NEEDS TO PUT IN A SIMILAR CHECK, NON EXISTENT USERS & USERS W 0 TWEETS CRASH CODE CURRENTLY
        if len(userdata['results']) == 0 or type(userdata['results']) is dict:
            return {}
        
        else:
            if (len(userdata['results']) > 0):
                created_at = tweetadder.replaceMonth(userdata['results'][0]['created_at'])
                cur_datetime = datetime.datetime(int(created_at[25:]), int(created_at[4:6]), int(created_at[7:9]),
                                   int(created_at[10:12]), int(created_at[13:15]), int(created_at[16:18]))
                num_days+=1
                user_name = userdata['results'][0]["user"]["screen_name"]
                
            for tweet in userdata['results']:
                created_at = tweetadder.replaceMonth(tweet['created_at'])
                created = datetime.datetime(int(created_at[25:]), int(created_at[4:6]), int(created_at[7:9]),
                                   int(created_at[10:12]), int(created_at[13:15]), int(created_at[16:18]))
                
                text = tweet['text']

                #update day count
                if created.day != cur_datetime.day or created.month != cur_datetime.month or created.year != cur_datetime.year:
                    cur_datetime = created
                    num_days+=1

                #update num_per_time count
                num_per_time[math.floor(created.hour / 4)] += 1

                #update num_per_weekday count
                num_per_weekday[created.weekday()]+=1

                #Get RT @ and # counts
                link = False
                mention = False
                rt = False
                has = False
                for word in text.split(" "):
                    if "http://" in word and not link:
                        num_links+=1
                        link = True
                        
                    if len(word) > 0 and word[0] == "@" and word[1:] != user_name:
                        mentions.append(word)
                        if not mention:
                            num_at +=1
                            mention = True

                    if "RT" == word and not rt:
                        num_rt+=1
                        rt = True
                        
                    if len(word) > 0 and word[0] == "#":
                        hashes.append(word)
                        if not has:
                            num_hash +=1
                            has = True
            
            mention_count = collections.Counter(mentions)
            unique_mentions = -1.0
            if len(mentions)!=0:
                unique_mentions = float(len(mention_count))/len(mentions)

            hash_count = collections.Counter(hashes)
            unique_hashes = -1.0
            if len(hashes)!=0:
                unique_hashes = float(len(hash_count))/len(hashes)

            total_tweets = len(userdata['results'])
            dicvals ={}
            if total_tweets != 0:
                dicvals = {"tr_day": float(total_tweets)/num_days,
                               "tr_monday": num_per_weekday[0]/total_tweets,
                               "tr_tuesday": num_per_weekday[1]/total_tweets,
                               "tr_wednesday": num_per_weekday[2]/total_tweets,
                               "tr_thursday": num_per_weekday[3]/total_tweets,
                               "tr_friday": num_per_weekday[4]/total_tweets,
                               "tr_saturday": num_per_weekday[5]/total_tweets,
                               "tr_sunday": num_per_weekday[6]/total_tweets,
                               "tr_latenight": num_per_time[0]/total_tweets,
                               "tr_earlymorning": num_per_time[1]/total_tweets,
                               "tr_morning": num_per_time[2]/total_tweets,
                               "tr_afternoon": num_per_time[3]/total_tweets,
                               "tr_evening": num_per_time[4]/total_tweets,
                               "tr_night": num_per_time[5]/total_tweets,
                               "mention_rate": float(num_at)/total_tweets,
                               "retweet_rate": float(num_rt)/total_tweets,
                               "hash_rate": float(num_hash)/total_tweets,
                               "link_rate": float(num_links)/total_tweets,
                               "unique_hash": unique_hashes,
                               "unique_mention": unique_mentions,
                               "user":user_name
                               }

            return dicvals

    def GetUserTFIDFs(self, userdata):
        tfidfobj = TfIdf()

        #GET TERM COUNTS AND BUILD DICS
        terms = {}
        token_mapping = {}
        user_tweets = {}
        
        for tweet in userdata['results']:
            user_tweets[tweet['id']] = tweet
            tokens = [unidecode.unidecode(t) for t in tfidfobj.get_tokens(tweet['text'],tagtypes=False,wordsonly=True,excludeUrls=True,minLength=3)]
            for token in tokens:
                if token in terms:
                    terms[token] += 1
                else:
                    terms[token] = 1

                if token in token_mapping:
                    token_mapping[token].append(tweet['id'])
                else:
                    token_mapping[token] = [tweet['id']]

        #CALCULATE TFIDF        
        idfs = DataGrabber().GetTermIDFs(terms.keys())
        scores = {}
    
        for term in terms.keys():
            if term in idfs['idfs']: 
                tf = float(terms[term]) / len(tokens)
                thistfidf = tf * float(idfs['idfs'][term])
                scores[term] = thistfidf

        dscores = [(term, scores[term]) for term in scores.keys()]
        dscores.sort(key=lambda x:-1*x[1])

        user_scores = {}
        for score in dscores:
            user_scores[score[0]] = score[1]

        return {'scores_dic':user_scores,
                'scores_list':dscores,
                'tweets':user_tweets,
                'token_mapping':token_mapping}

    def GetTermIDFs(self, terms):
        
        url = 'http://lemurturtle.com/idf.php?'
        data = ('terms='+','.join(terms).replace("#","%23")).encode('latin1')
        print(data)

        txt = urllib.request.urlopen(url,data).read().decode('latin1')
            
        txt = txt.replace(",null:",',"null":') #workaround
        data = json.loads(txt)
        return data;


    def GetCelebTFIDFsForTerms(self, terms):
        q = "SELECT * FROM celeb_tfidf WHERE score > .005 AND token IN("
        count = 0
        vals = {}
        for term in terms:
            vals['token'+str(count)] = unidecode.unidecode(term)
            q += "%(token"+str(count)+")s,"
            
            count += 1

        q = q[:len(q)-1] #remove last comma
        q += ") ORDER BY score DESC"
        results = self.sql.q(q, vals)

        return results

    def GetCelebTweetStats(self):
        q = "SELECT * FROM celeb_stats WHERE tr_day > -1"
        results = self.sql.q(q)

        return results

    def GetCelebMatchesForUser(self, user):
        results = {
            'user':
                {
                    'screen_name' : user,
                    'name' : '',
                    'pic_url' : ''
                },
            'celeb_matches': []
        }

        #GET USER TWEETS
        userdata = self.GetUserTweets(user)

        results['user']['name'] = userdata['results'][0]['user']['name']
        results['user']['pic_url'] = userdata['results'][0]['user']['profile_image_url']

        #Pass User Stats To Get Celeb Matches
        celebstats = self.GetCelebTweetStats()
        
        celebmatches = celebmatcher.getCelebMatches(userstats, celebstats)
        pprint.pprint(celebmatches)

        #GET USER TWEET STATS
        #userstats = self.GetUserTweetStats(userdata)
        #pprint.pprint(userstats)

        #GET CELEB STATS
        

        #CALCULATE TWEET STAT MATCH SCORES
        

        #GET USER TFIDF
        usertfidf = self.GetUserTFIDFs(userdata)
        userscores = usertfidf['scores_dic']

        print("top user terms are",usertfidf['scores_list'][:15])

        #GET CELEBS TFIDF
        celebscores = self.GetCelebTFIDFsForTerms([term[0] for term in usertfidf['scores_list']][:15])

        #CALCULATE MATCH SCORES

        cumcelebscores = {}
        celebwords = {}
        for entry in celebscores:
            celeb = entry[0]
            token = unidecode.unidecode(entry[1])
            score = float(entry[2])

            if celeb in cumcelebscores:
                celebwords[celeb][token] = score
                cumcelebscores[celeb] += userscores[token] * score
            else:
                celebwords[celeb] = {token:score}
                cumcelebscores[celeb] = userscores[token] * score

        matches = [(celeb, cumcelebscores[celeb], celebwords[celeb]) for celeb in cumcelebscores]
        matches.sort(key=lambda x: -cumcelebscores[x[0]])

        #FIND MATCHING TWEETS FOR TOP 10 CELEBS
        for i in range(10):
            celeb_match =  {
                        'screen_name' : matches[i][0],
                        'name' : '',
                        'pic_url' : '',
                        'match_score':cumcelebscores[matches[i][0]],
                        'top_words' : matches[i][2],
                        'tweets' : []
                    }

            vals = {'celeb':matches[i][0], 'tokens': ' '.join(matches[i][2])}
            q = "SELECT text FROM tweets WHERE from_user=%(celeb)s AND MATCH(text) AGAINST(%(tokens)s)"
            matching_celeb_tweets = [result[0] for result in self.sql.q(q,vals)]
            #pprint.pprint(results)
            matches[i] = list(matches[i])
            
            matching_user_tweets = [usertfidf['tweets'][usertfidf['token_mapping'][unidecode.unidecode(token)][0]]['text'] for token in matches[i][2]]

            #ADD TWEETS THAT MATCH ON TOKENS
            sorted_tokens = [token for token in  sorted(matches[i][2].keys(), key=lambda x: -matches[i][2][x])]
            #for token in matches[i][2]:
            for token in sorted_tokens:
                celeb_tweets_for_token = list(filter(lambda x: x.count(token) > 0, matching_celeb_tweets))
                user_tweets_for_token = [usertfidf['tweets'][usertfidf['token_mapping'][token][k]] for k in range(len(usertfidf['token_mapping'][token]))]

                for j in range(min(len(celeb_tweets_for_token), len(user_tweets_for_token))):
                    celeb_match['tweets'].append(
                        {
                            'word' : token,
                            'user_tweet':
                                {
                                    'url': 'http://twitter.com/'+user_tweets_for_token[j]['user']['screen_name']+'/status/'+str(user_tweets_for_token[j]['id']),
                                    'text': user_tweets_for_token[j]['text']
                                },
                            'celeb_tweet':
                                {
                                    'url': 'http://twitter.com/'+matches[i][0],
                                    'text': celeb_tweets_for_token[j]
                                }
                        })


            matches[i].append({matches[i][0]:matching_celeb_tweets,user:matching_user_tweets})

            if len(celeb_match['tweets']) != 0:
                results['celeb_matches'].append(celeb_match)



        #return matches
        return results

        

if __name__ == '__main__':
    #jbtweets = DataGrabber().GetTweetsForUser("justinbieber")
    #pprint.pprint(jbtweets)
    #print(len(jbtweets))
    #DoSomeShit()
    #DoSomeOtherShit()
    #DataGrabber().GenerateLDAData()
    #DataGrabber().GetTfIdfScores()

    #user = "KingGails"
    #user = "King32David"
    #user = "joshrweinstein"
    #user = "simplycary"
    #user = "Live_2Belieb"
    #user = "iluvjb1518"
    #user = "Belieb_Forever"
    #user = "sbilstein"
    #user = "boomshakanaka"
    #user = "nuqb"
    #user = "celebjelly"
    #user = "jonslaught"
    #user = "Tach_0"
    #user = "EmilyAnneNichol"
    #user = "james_quinlan"
    #user = "ggrenley"
    #user = "Suciaaaaa"

    #user = "dulcineadelech"
    #user = "pr0crastin8r"

    #user = "cooper_carter"
    user = "ava361"

    #non existent user for testing
    #user = "nonexistent75756fj"

    #user with 0 tweets for testing
    #user = "Adared"

    #pprint.pprint(DataGrabber().GetCelebMatchesForUser(user)[:10])
    pprint.pprint(DataGrabber().GetCelebMatchesForUser(user))
    
    
    #pprint.pprint(DataGrabber().GetCelebTFIDFsForTerms(["weed"]))    
    

    
