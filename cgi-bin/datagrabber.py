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
import debuglog

class DataGrabber:
    def __init__(self):
        self.sql = SQLQuery()
        self.tf = TweetFetcher()

    def GetTweetsForUser(self, username):
        q = "SELECT (text) FROM tweets WHERE from_user=%s"
        v = username
        results = self.sql.q(q,v)
        return results
        
    def GetAllText(self):
        q = "SELECT text FROM tweets"
        return self.sql.q(q)

    def GenerateLDAData(self):
        """
        Output tab-separated file to be consumed by LDA.
        """
        f = open('ldadata.tsv','w')
        q = "SELECT id, text FROM tweets"
        data = self.sql.q(q)

        # TODO: Unify encoding strategy.
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
                       debuglog.msg("One tough cookie! Couldn't decode this:",d)

        f.close()
        debuglog.msg('done writing LDA data to file!')

    def GetUserTweets(self, user, canretry=True):
        userdata = None
        if self.tf.canFetchTimeline():
            userdata = self.tf.fetchUserTimeline(user, format="searchapi", use_filesystem_cache=True)
        else:
            userdata = self.tf.getUserTweetsData(user)

        if 'results' not in userdata:
            if canretry:
                return self.GetUserTweets(user, canretry=False)
            else:
                userdata = self.tf.getUserTweetsData(user)

        return userdata

    
    def GetUserTFIDFs(self, userdata):
        tfidfobj = TfIdf()

        # GET TERM COUNTS AND BUILD DICS
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
        url = 'http://50.56.221.228/cgi-bin/idf.php?'
        # TODO: Unify encoding strategy.
        data = ('terms='+','.join(terms).replace("#","%23")).encode('latin1')
        debuglog.msg(data)

        txt = urllib.request.urlopen(url,data).read().decode('latin1')
            
        txt = txt.replace(",null:",',"null":') #workaround
        data = json.loads(txt)
        return data


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
        """
        Generate object with information about user and matches with celeb (including matching tweets) to pass to the
        UI.
        """
        
        results = {
            'user':
                {
                    'screen_name' : user,
                    'name' : '',
                    'pic_url' : '',
                    'personality' : ''
                },
            'celeb_matches': [],
            'celeb_matches_pers' : []
        }

        # GET USER TWEETS
        user_data = self.GetUserTweets(user)

        # return an error if user doesn't exist/has no tweets.
        if user_data is None or not len(user_data['results']):
            results['status'] = 'error'
            return results

        results['user']['name'] = user_data['results'][0]['user']['name']
        results['user']['pic_url'] = user_data['results'][0]['user']['profile_image_url']

        #Pass user_data and celeb_stats to get celeb matches
        celeb_stats = self.GetCelebTweetStats()
        celeb_matches = celebmatcher.getCelebMatches(user_data, celeb_stats)

        results['user']['personality'] = celeb_matches[0]
        results['celeb_matches_pers'] = celeb_matches[1]

        # GET USER TFIDF
        user_tfidf = self.GetUserTFIDFs(user_data)
        user_scores = user_tfidf['scores_dic']

        debuglog.msg("top user terms are",user_tfidf['scores_list'][:15])

        # GET CELEBS TFIDF
        celeb_scores = self.GetCelebTFIDFsForTerms([term[0] for term in user_tfidf['scores_list']][:15])

        # CALCULATE MATCH SCORES
        cumulative_celeb_scores = {}
        celeb_words = {}
        for entry in celeb_scores:
            celeb = entry[0]
            token = unidecode.unidecode(entry[1])
            score = float(entry[2])

            if celeb in cumulative_celeb_scores:
                celeb_words[celeb][token] = score
                cumulative_celeb_scores[celeb] += user_scores[token] * score
            else:
                celeb_words[celeb] = { token:score }
                cumulative_celeb_scores[celeb] = user_scores[token] * score

        matches = [(celeb, cumulative_celeb_scores[celeb], celeb_words[celeb]) for celeb in cumulative_celeb_scores]
        matches.sort(key=lambda x: -cumulative_celeb_scores[x[0]])

        # FIND MATCHING TWEETS FOR TOP 10 CELEBS
        for top_10_celeb_index in range(10):
            celeb_match =  {
                        'screen_name' : matches[top_10_celeb_index][0],
                        'name' : '',
                        'pic_url' : '',
                        'match_score':cumulative_celeb_scores[matches[top_10_celeb_index][0]],
                        'top_words' : matches[top_10_celeb_index][2],
                        'tweets' : []
                    }

            vals = {'celeb':matches[top_10_celeb_index][0], 'tokens': ' '.join(matches[top_10_celeb_index][2])}
            q = "SELECT text, id, from_user_name, profile_image_url FROM tweets WHERE from_user=%(celeb)s AND MATCH(text) AGAINST(%(tokens)s)"
            q_results = self.sql.q(q, vals)

            # skip if we don't have any matching celeb tweets.
            if not len(q_results):
                continue

            celeb_match['name'] = q_results[0][2]
            celeb_match['pic_url'] = q_results[0][3]
            matching_celeb_tweets = [{'text':result[0], 'id':result[1]} for result in q_results]

            matches[top_10_celeb_index] = list(matches[top_10_celeb_index])
            
            #matching_user_tweets = [user_tfidf['tweets'][user_tfidf['token_mapping'][unidecode.unidecode(token)][0]]['text']
            #                        for token in matches[top_10_celeb_index][2]]

            # ADD TWEETS THAT MATCH ON TOKENS
            sorted_tokens = [token for token in  sorted(matches[top_10_celeb_index][2].keys(), key=lambda x: -matches[top_10_celeb_index][2][x])]
            for token in sorted_tokens:
                celeb_tweets_for_token = list(filter(lambda x: x['text'].count(token) > 0, matching_celeb_tweets))
                user_tweets_for_token = [user_tfidf['tweets'][user_tfidf['token_mapping'][token][k]]
                                         for k in range(len(user_tfidf['token_mapping'][token]))]

                for matching_tweets_for_token_index in range(min(len(celeb_tweets_for_token), len(user_tweets_for_token))):
                    celeb_match['tweets'].append(
                        {
                            'word' : token,
                            'user_tweet':
                                {
                                    'url': 'http://twitter.com/' +
                                                user_tweets_for_token[matching_tweets_for_token_index]['user']['screen_name'] +
                                                '/status/' +
                                                str(user_tweets_for_token[matching_tweets_for_token_index]['id']),
                                    'text': user_tweets_for_token[matching_tweets_for_token_index]['text']
                                },
                            'celeb_tweet':
                                {
                                    'url': 'http://twitter.com/' +
                                                celeb_match['screen_name'] +
                                                '/status/' +
                                                str(celeb_tweets_for_token[matching_tweets_for_token_index]['id']),
                                    'text': celeb_tweets_for_token[matching_tweets_for_token_index]['text']
                                }
                        })


            #matches[top_10_celeb_index].append({matches[top_10_celeb_index][0]:matching_celeb_tweets,user:matching_user_tweets})

            if len(celeb_match['tweets']):
                results['celeb_matches'].append(celeb_match)

        results['status'] = 'ok'
        return results

        

if __name__ == '__main__':
    #jbtweets = DataGrabber().GetTweetsForUser("justinbieber")
    #debuglog.pprint_msg(jbtweets)
    #print(len(jbtweets))
    #DoSomeShit()
    #DoSomeOtherShit()
    #DataGrabber().GenerateLDAData()
    #DataGrabber().GetTfIdfScores()

    #user = "KingGails"
    user = "King32David"
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
    #user = "ava361"
    #user = "JonathanPezzino"

    #non existent user for testing
    #user = "nonexistent75756fj"

    #user with 0 tweets for testing
    #user = "Adared"

    pprint.pprint(DataGrabber().GetCelebMatchesForUser(user))
    
    
    #pprint.pprint(DataGrabber().GetCelebTFIDFsForTerms(["weed"]))
    

    
