from dbsql import *
import pprint, collections, datetime

class TweetStatGenerator:
    def __init__(self):
        self.sql = SQLQuery()


    def genStats(self, user_name):
        """
        Generates Twitter Statistics About a user
        """

        #create SQL query to get all tweets from user
        q = "SELECT created_at,source,text,to_user FROM tweets WHERE from_user = '" + user_name +"' ORDER BY created_at"
        tweets = self.sql.q(q)

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
            source = tweet[1]
            text = tweet[2]
            to_user = tweet[3]

            #update day count
            if created.day != cur_datetime.day or created.month != cur_datetime.month or created.year != cur_datetime.year:
                cur_datetime = created
                num_days+=1

            #update num_per_time count
            num_per_time[created.hour / 4] += 1

            #update num_per_weekday count
            num_per_weekday[created.weekday()]+=1

            if "@" in text: #this is not strictly correct, @ can appear in text body
                num_at+=1
                for w in text.split(" "):
                    if len(w) > 0 and w[0] == "@" and w[1:] != user_name:
                        mentions.append(w)

            if "RT " in text: #this is not strictly correct, RT can appear in text body
                num_rt+=1

            if "#" in text: #this is not strictly correct, # can appear in text body
                num_hash+=1
                for w in text.split(" "):
                    if len(w) > 0 and w[0] == "#":
                        hashes.append(w)

            if "http://" in text:
                num_links+=1

        mention_count = collections.Counter(mentions)
        hash_count = collections.Counter(hashes)
        total_tweets = len(tweets)
        
        output_dict = {"Tweets Per Day": float(total_tweets)/num_days,
                       "Tweet Rate Monday": num_per_weekday[0]/total_tweets,
                       "Tweet Rate Tuesday": num_per_weekday[1]/total_tweets,
                       "Tweet Rate Wednesday": num_per_weekday[2]/total_tweets,
                       "Tweet Rate Thursday": num_per_weekday[3]/total_tweets,
                       "Tweet Rate Friday": num_per_weekday[4]/total_tweets,
                       "Tweet Rate Saturday": num_per_weekday[5]/total_tweets,
                       "Tweet Rate Sunday": num_per_weekday[6]/total_tweets,
                       "Tweet Rate Late Night": num_per_time[0]/total_tweets,
                       "Tweet Rate Early Morning": num_per_time[1]/total_tweets,
                       "Tweet Rate Morning": num_per_time[2]/total_tweets,
                       "Tweet Rate Afternoon": num_per_time[3]/total_tweets,
                       "Tweet Rate Evening": num_per_time[4]/total_tweets,
                       "Tweet Rate Night": num_per_time[5]/total_tweets,
                       "Mention Rate": float(num_at)/total_tweets,
                       "Retweet Rate": float(num_rt)/total_tweets,
                       "Hash Rate": float(num_hash)/total_tweets,
                       "Link Rate": float(num_links)/total_tweets,
                       "Unique Hash %": float(len(hash_count))/len(hashes),
                       "Unique Mention %": float(len(mention_count))/len(mentions)
                       }
            
        pprint.pprint(output_dict)


if __name__ == '__main__':
    tg = TweetStatGenerator();
    tg.genStats("charliesheen")
