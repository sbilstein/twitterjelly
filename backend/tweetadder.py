from dbsql import *
import pickle
import pprint
import datetime
from unidecode import unidecode
from tfidf import TfIdf
import time

def replaceMonth(datetimestr):
    monthnums = [("Jan","01"),("Feb","02"),("Mar","03"),("Apr","04"),("May","05"),("Jun","06"),("Jul","07"),("Aug","08"),("Sep","09"),("Oct","10"),("Nov","11"),("Dec","12")]
    for monthnum in monthnums:
        datetimestr = datetimestr.replace(monthnum[0],monthnum[1])
    return datetimestr;
                             

class TweetAdder:
    def __init__(self):
        self.sql = SQLQuery()
        self.tfidfobj = TfIdf()

        self.ids = [i[0] for i in self.sql.q("SELECT id FROM tweets")]

    def addTimelineTweet(self, timelinetweet):
        '''converts timeline tweet to search api format and adds it'''
        tweet = {}
        created_at = replaceMonth(timelinetweet['created_at'])
        dt = datetime.datetime(int(created_at[25:]), int(created_at[4:6]), int(created_at[7:9]),
                               int(created_at[10:12]), int(created_at[13:15]), int(created_at[16:18]))
        tweet['created_at'] = dt
                               
        tweet['from_user']         = timelinetweet['user']['screen_name']
        tweet['from_user_id']      = timelinetweet['user']['id']
        tweet['from_user_name']    = timelinetweet['user']['name']
        tweet['geo']               = timelinetweet['user']['location']
        tweet['id']                = timelinetweet['id']
        tweet['iso_language_code'] = timelinetweet['user']['lang']
        tweet['metadata']          = {'result_type':'timeline'}
        tweet['profile_image_url'] = timelinetweet['user']['profile_image_url']
        tweet['source']            = timelinetweet['source']
        tweet['text']              = timelinetweet['text']
        tweet['to_user']           = timelinetweet['in_reply_to_screen_name']
        tweet['to_user_id']        = timelinetweet['in_reply_to_user_id']
        tweet['to_user_name']      = None

        self.add(tweet, created_at_is_obj=True)
        
    def add(self, tweet, created_at_is_obj=False):
        '''adds a tweet in the format provided by search api'''
        print("inserting tweet", tweet['id'])
        #pprint.pprint(tweet)

        if not created_at_is_obj:
            dt = datetime.datetime.strptime(replaceMonth(tweet['created_at'][5:25]),"%d %m %Y %H:%M:%S")
        else:
            dt = tweet['created_at']
            
        created_at = dt.strftime("%Y-%m-%d %H:%M:%S")
        
        dicvals = {'created_at':created_at,
                'from_user':tweet['from_user'],
                'from_user_id':tweet['from_user_id'],
                    'from_user_name':tweet['from_user_name'],
                    'geo':str(tweet['geo']),
                    'id':tweet['id'],
                    'iso_language_code':tweet['iso_language_code'],
                    'metadata':str(tweet['metadata']),
                    'profile_image_url':tweet['profile_image_url'],
                    'source':tweet['source'],
                    'text':tweet['text'],
                    'to_user':tweet['to_user'],
                    'to_user_id':tweet['to_user_id'],
                    'to_user_name':tweet['to_user_name']}

    

                                
        dicq= """INSERT IGNORE INTO tweets VALUES(%(created_at)s,
                                            %(from_user)s,
                                            %(from_user_id)s,
                                            %(from_user_name)s,
                                            %(geo)s,
                                            %(id)s,
                                            %(iso_language_code)s,
                                            %(metadata)s,
                                            %(profile_image_url)s,
                                            %(source)s,
                                            %(text)s,
                                            %(to_user)s,
                                            %(to_user_id)s,
                                            %(to_user_name)s)"""

        #checkexists = self.sql.q("SELECT id FROM tweets WHERE id=%s",tweet['id'])

        
        if tweet['id'] not in self.ids:
            succeeded = False
            try:
                self.sql.q(dicq,dicvals)
                succeeded = True
            except UnicodeEncodeError:
                try:
                    print("UNIDECODE ERROR, trying decode...")
                    for k in dicvals:
                        dicvals[k] = unidecode(dicvals[k])
                    self.sql.q(dicq,dicvals)
                    succeeded = True
                except:
                    print("Unidecode failed :(")

            
            if succeeded:
                tokens = self.tfidfobj.get_tokens(tweet['text'])
                self.addTokens(tweet,tokens)
                self.addTokenMapping(tweet, tokens)

            return succeeded

        print("tweet already existed")
        return False

    def addTokens(self, tweet, tokens=None):
        if tokens is None:
            txt = tweet['text']
            tokens = self.tfidfobj.get_tokens(txt)
        
        count = 0
        vals = {}
        q =  "INSERT IGNORE INTO tokens (token, type) VALUES"

        for token in tokens:
            #print(token)
            vals['token'+str(count)] = token[0]
            vals['type'+str(count)] = token[1]
            q += "(%(token"+str(count)+")s, %(type"+str(count)+")s),"
            count += 1
            
        q = q[:len(q)-1] #remove last comma
        self.sql.q(q,vals)

    def addTokenMapping(self, tweet, tokens=None):
        if tokens is None:
            txt = tweet['text']
            tokens = self.tfidfobj.get_tokens(txt)

        count = 0
        vals = {'user':tweet['from_user']}            
        q = "INSERT INTO token_user_mapping (user, token) VALUES"
        for token in tokens:
            q += "(%(user)s, %(token"+str(count)+")s),"
            vals['token'+str(count)] = token[0]
            count+=1

        #print("token mapping query",q)
        q = q[:len(q)-1] #remove last comma
        self.sql.q(q,vals)

    def fixRackSpaceDB(self):
        q = "SELECT text, from_user, id FROM tweets";

        results = self.sql.q(q)
        failures = []
        f = open('token_fix_failures.txt','w')
        for result in results:
            print("Adding tokens for tweet",result[2])
            try:
                self.addTokens({'text':result[0], 'from_user':result[1]})
                self.addTokenMapping({'text':result[0], 'from_user':result[1]})
            except:
                failures.append(result[2])
                print("\tAdding tokens failed!")
                print("\tFailures so far:",len(failures))
                f.write(result[2]+"\n")

        f.close()

        print(failures)




if __name__ == '__main__':
    TweetAdder().fixRackSpaceDB()