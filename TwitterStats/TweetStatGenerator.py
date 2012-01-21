from dbsql import *
import pprint, collections, datetime

class TweetStatGenerator:
    def __init__(self):
        self.sql = SQLQuery()

    def createStatDB(self):
        q = "SELECT * FROM celebs"
        celebs = self.sql.q(False,q)

        for celeb in celebs:
            self.genStats(celeb[0])

    def genStats(self, user_name):
        """
        Generates Twitter Statistics About a user & Pushes to MYSQL DB
        """

        #create SQL query to get all tweets from user
        q = "SELECT created_at,text FROM tweets WHERE from_user=%(user_name)s ORDER BY created_at"
        vals = {'user_name':user_name}
        tweets = self.sql.q(False,q,vals)

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

        if (len(tweets) > 0):
            cur_datetime = tweets[0][0]
            num_days+=1

        for tweet in tweets:
            created = tweet[0]
            text = tweet[1]

            #update day count
            if created.day != cur_datetime.day or created.month != cur_datetime.month or created.year != cur_datetime.year:
                cur_datetime = created
                num_days+=1

            #update num_per_time count
            num_per_time[created.hour / 4] += 1

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

        total_tweets = len(tweets)
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
        else:
            dicvals = {"tr_day": -1.0,
                           "tr_monday": -1.0,
                           "tr_tuesday": -1.0,
                           "tr_wednesday": -1.0,
                           "tr_thursday":-1.0,
                           "tr_friday": -1.0,
                           "tr_saturday": -1.0,
                           "tr_sunday": -1.0,
                           "tr_latenight": -1.0,
                           "tr_earlymorning": -1.0,
                           "tr_morning": -1.0,
                           "tr_afternoon": -1.0,
                           "tr_evening": -1.0,
                           "tr_night": -1.0,
                           "mention_rate": -1.0,
                           "retweet_rate": -1.0,
                           "hash_rate": -1.0,
                           "link_rate": -1.0,
                           "unique_hash": -1.0,
                           "unique_mention": -1.0,
                           "user":user_name
                           }

        #insert dictionary into DB
        print("inserting user ",user_name)
        
        #the query needs to be REPLACE if unique key already existS!                         
        dicq= """INSERT INTO celeb_stats VALUES(%(tr_day)s,
                                            %(tr_monday)s,
                                            %(tr_tuesday)s,
                                            %(tr_wednesday)s,
                                            %(tr_thursday)s,
                                            %(tr_friday)s,
                                            %(tr_saturday)s,
                                            %(tr_sunday)s,
                                            %(tr_latenight)s,
                                            %(tr_earlymorning)s,
                                            %(tr_morning)s,
                                            %(tr_afternoon)s,
                                            %(tr_evening)s,
                                            %(tr_night)s,
                                            %(mention_rate)s,
                                            %(retweet_rate)s,
                                            %(hash_rate)s,
                                            %(link_rate)s,
                                            %(unique_hash)s,
                                            %(unique_mention)s,
                                            %(user)s)
                    ON DUPLICATE KEY UPDATE tr_day=%(tr_day)s,
                                            tr_monday=%(tr_monday)s,
                                            tr_tuesday=%(tr_tuesday)s,
                                            tr_wednesday=%(tr_wednesday)s,
                                            tr_thursday=%(tr_thursday)s,
                                            tr_friday=%(tr_friday)s,
                                            tr_saturday=%(tr_saturday)s,
                                            tr_sunday=%(tr_sunday)s,
                                            tr_latenight=%(tr_latenight)s,
                                            tr_earlymorning=%(tr_earlymorning)s,
                                            tr_morning=%(tr_morning)s,
                                            tr_afternoon=%(tr_afternoon)s,
                                            tr_evening=%(tr_evening)s,
                                            tr_night=%(tr_night)s,
                                            mention_rate=%(mention_rate)s,
                                            retweet_rate=%(retweet_rate)s,
                                            hash_rate=%(hash_rate)s,
                                            link_rate=%(link_rate)s,
                                            unique_hash=%(unique_hash)s,
                                            unique_mention=%(unique_mention)s"""


        succeeded = False
        try:
            self.sql.q(True,dicq,dicvals)
            succeeded = True
            print "Success"
        except UnicodeEncodeError:
            try:
                print("UNIDECODE ERROR, trying decode...")
                for k in dicvals:
                    dicvals[k] = unidecode(dicvals[k])
                self.sql.q(dicq,dicvals)
                succeeded = True
            except:
                print("Unidecode failed :(")

        return succeeded


if __name__ == '__main__':
    tg = TweetStatGenerator()
    #tg.genStats("ladygaga")
    tg.createStatDB()

