from dbsql import *
import pickle
import pprint
from unidecode import unidecode
import debuglog

sql = SQLQuery()

db = pickle.load(open("tweets_db.pkl","rb"))
ids = sql.q("SELECT id FROM tweets")
ids = [i[0] for i in ids]
for tweetid in db:
    tweet = db[tweetid]
    print("inserting tweet:")
    debuglog.pprint_msg(tweet)
    
    dicvals = {'created_at':tweet['created_at'],
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

                                
    dicq= """INSERT INTO tweets VALUES(%(created_at)s,
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

    #print(tweet['id'],ids)
    if tweet['id'] not in ids:
        try:
            sql.q(dicq,dicvals)
        except UnicodeEncodeError:
            try:
                print("UNIDECODE ERROR, trying decode...")
                for k in dicvals:
                    dicvals[k] = unidecode(dicvals[k])
                sql.q(dicq,dicvals)
            except:
                print("Unidecode failed :(")
                                
