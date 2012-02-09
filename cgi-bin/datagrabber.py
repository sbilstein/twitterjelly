from dbsql import *
from tfidf import *
import unidecode
import urllib.request
import json
from util import *
from fetchtweets import TweetFetcher
import hashlib
import celebmatcher
import debuglog
from dammit import UnicodeDammit
from decimal import *

class DataGrabber:
    #@perftest
    def __init__(self):
        self.sql = SQLQuery()
        self.tf = TweetFetcher(sql_obj=self.sql)

    #@perftest
    def GetUserTweets(self, user, can_retry=True):
        user_data = None
        if self.tf.canFetchTimeline():
            user_data = self.tf.fetchUserTimeline(user, format="searchapi", use_filesystem_cache=True)
        else:
            user_data = self.tf.getUserTweetsData(user)

        if 'results' not in user_data:
            if 'error' in user_data:
                ret = {'status':'error'}
                if user_data['error'] == 'Not authorized':
                    ret['error'] = 'protected'
                return ret
            if can_retry:
                return self.GetUserTweets(user, can_retry=False)
            else:
                user_data = self.tf.getUserTweetsData(user)
        elif not len(user_data['results']):
            ret = {'status':'error', 'error':'no_tweets'}
            return ret

        return user_data

    #@perftest
    def GetUserTFIDFs(self, user_data):
        tfidf_obj = TfIdf()

        # GET TERM COUNTS AND BUILD DICTS
        terms = {}
        token_mapping = {}
        user_tweets = {}

        for tweet in user_data['results']:
            user_tweets[tweet['id']] = tweet

            tokens = [t for t in tfidf_obj.get_tokens(tweet['text'],
                                                      tagtypes=False, wordsonly=True, excludeUrls=True, minLength=3)]

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
        idfs = self.GetTermIDFs(terms.keys())
        scores = {}
    
        for term in terms.keys():
            if term in idfs['idfs']: 
                tf = Decimal(terms[term]) / Decimal(len(tokens))
                this_tfidf = Decimal(tf) * Decimal(idfs['idfs'][term])
                scores[term] = float(this_tfidf)

        sorted_scores = [(term, scores[term]) for term in scores.keys()]
        sorted_scores.sort(key=lambda x:-1*x[1])

        user_scores = {}
        for score in sorted_scores:
            user_scores[score[0]] = score[1]

        return {'scores_dic':user_scores,
                'scores_list':sorted_scores,
                'tweets':user_tweets,
                'token_mapping':token_mapping}

    #@perftest
    def GetTermIDFs(self, terms):
        if not terms or not len(terms):
            return json.loads({"idfs":[]})

        url = 'http://50.56.221.228/cgi-bin/idf.php?'
        # TODO: HTML entity encoding (?)
        # TODO: Enhanced encoding detection - first term's encoding may not be always appropriate.
        data = ('terms='+','.join(terms).replace("#","%23")).encode("utf-8")
        debuglog.msg(data)

        txt_unicode = UnicodeDammit(urllib.request.urlopen(url,data).read())
        txt = txt_unicode.unicode_markup
        txt = txt.replace(",null:",',"null":') #workaround
        data = json.loads(txt, encoding=txt_unicode.original_encoding)
        return data

    #@perftest
    def GetCelebTFIDFsForTerms(self, terms):
        q = "SELECT * FROM celeb_tfidf WHERE token IN("
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

    #@perftest
    def GetCelebTweetStats(self):
        q = "SELECT * FROM celeb_stats WHERE tr_day > -1"
        results = self.sql.q(q)

        return results

    #@perftest
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

            if celeb.lower() == user.lower():
                continue

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

            # ADD TWEETS THAT MATCH ON TOKENS
            sorted_tokens = [token for token in  sorted(matches[top_10_celeb_index][2].keys(), key=lambda x: -matches[top_10_celeb_index][2][x])]
            for token in sorted_tokens:
                celeb_tweets_for_token = list(filter(lambda x: x['text'].lower().count(token.lower()) > 0, matching_celeb_tweets))
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
        results['permalink_id'] = self.StorePermalink(results)
        return results

    def StorePermalink(self, results_obj):
        json_txt = json.dumps(results_obj)
        hash = hashlib.md5(json_txt.encode('utf-8')).hexdigest()
        q  = "INSERT INTO stored_matches_json (hash, user, json) VALUES(%(hash)s, %(user)s, %(json)s);"
        vals = {'user' : results_obj['user']['screen_name'], 'json':json_txt, 'hash':hash}

        self.sql.q(q, vals)
        return hash

if __name__ == '__main__':
    #jbtweets = DataGrabber().GetTweetsForUser("justinbieber")
    #debuglog.pprint_msg(jbtweets)
    #print(len(jbtweets))
    #DoSomeShit()
    #DoSomeOtherShit()
    #DataGrabber().GenerateLDAData()
    #DataGrabber().GetTfIdfScores()

    user = "liltunechi"
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
    #user2 = "Suciaaaaa"
    #user = "tjfaust"

    #user2 = "dulcineadelech"
    #user = "pr0crastin8r"

    #user2 = "cooper_carter"
    #user = "ava361"
    #user = "JonathanPezzino"

    #non existent user for testing
    #user = "nonexistent75756fj"

    #user with 0 tweets for testing
    #user = "Adared"

    #user = "adamcarolla"
    #user = "robdelaney"
    #user = "2chambers"

    #dg = DataGrabber()
    #testPerfWithExistingDataGrabber(dg, user)
    #pprint.pprint(dg.GetCelebMatchesForUser(user))
    #pprint.pprint(dg.GetCelebMatchesForUser(user2))
    #pprint.pprint(DataGrabber().GetCelebTFIDFsForTerms(["weed"]))
    #testGetMatchFromFresh(user)
    #testPerfWithExistingDataGrabber(dg, user)
    testGetMatchFromFresh(user)

    
