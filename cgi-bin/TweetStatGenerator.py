from dbsql import *
import pprint, collections, datetime, math

class TweetStatGenerator:
    def __init__(self):
        self.sql = SQLQuery()


    def genPersonalityColumns(self,celebs):

        for cur in celebs:
            if cur[0] != -1:

                #calculate first personality dimension based on habits
                #get average tweet rates
                m_thu = sum(cur[1:5])/4.0
                fr_su = sum(cur[5:8])/3.0
                day = sum(cur[11:14])/3.0
                night = sum(cur[9:11],cur[14])/3.0

                #avg tweet rate on time off
                tr_weekend = (fr_su + night)/2.0
                tr_weekday = (m_thu + day)/2.0

                if tr_weekday > tr_weekend:
                    dim_1 = A
                else:
                    dim_1 = E

                #calculate other dimensions                
                P_m = cur[21]
                P_h = cur[22]
                P_l = cur[23]
                P_um = cur[24]
                P_uh = cur[25]

                if P_l > float(50.0):
                    dim_1 = "S"
                else:
                    print(P_l)
                    dim_1 = "C"

                if (P_m + P_um)/float(2.0) > float(50.0):
                    dim_2 = "W"
                else:
                    dim_2 = "T"

                if (P_h + P_uh)/float(2.0) > float(50.0):
                    dim_3 = "J"
                else:
                    dim_3 = "M"

                print("inserting personality dimensions user ",cur[20])

                
                dicvals = { "dim_1": dim_1,
                            "dim_2": dim_2,
                            "dim_3": dim_3,
                            "user": cur[20]}
                                        
                dicq= """UPDATE celeb_stats SET dim_1 = %(dim_1)s,
                                                dim_2 = %(dim_2)s,
                                                dim_3 = %(dim_3)s
                                            WHERE user = %(user)s """

                
                try:
                    self.sql.q(dicq,dicvals)
                    print("Success")
                except UnicodeEncodeError:
                    try:
                        print("UNIDECODE ERROR, trying decode...")
                        for k in dicvals:
                            dicvals[k] = unidecode(dicvals[k])
                        self.sql.q(dicq,dicvals)
                        succeeded = True
                    except:
                        print("Unidecode failed :(")

                

    def genPercentileColumns(self,celebs):

        for cur in celebs:
            #if we have no tweets from this celeb
            if cur[0] != -1:
                N = 0
                B_m = 0
                E_m = 0
                B_h = 0
                E_h = 0
                B_l = 0
                E_l = 0
                B_um = 0
                E_um = 0
                B_uh = 0
                E_uh = 0

                #go through celeb list calculating percentiles
                for celeb in celebs:
                    if celeb[0] == -1:
                        continue

                    #counts for percentiles
                    N += 1
                    if celeb[14] < cur[14]:
                        B_m += 1
                    elif celeb[14] == cur[14]:
                        E_m += 1

                    if celeb[16] < cur[16]:
                        B_h += 1
                    elif celeb[16] == cur[16]:
                        E_h += 1

                    if celeb[17] < cur[17]:
                        B_l += 1
                    elif celeb[17] == cur[17]:
                        E_l += 1

                    if celeb[18] < cur[18]:
                        B_uh += 1
                    elif celeb[18] == cur[18]:
                        E_uh += 1

                    if celeb[19] < cur[19]:
                        B_um += 1
                    elif celeb[19] == cur[19]:
                        E_um += 1

                    

                #CALCULATE PERCENTILES
                P_m = ((B_m + 0.5*E_m)/N)*100
                P_h = ((B_h + 0.5*E_h)/N)*100
                P_l = ((B_l + 0.5*E_l)/N)*100
                P_um = ((B_um + 0.5*E_um)/N)*100
                P_uh = ((B_uh + 0.5*E_uh)/N)*100

                #insert percentiles into db
                print("updating user ",cur[20])

            
                dicvals = { "P_m": P_m,
                            "P_h": P_h,
                            "P_l": P_l,
                            "P_um": P_um,
                            "P_uh": P_uh,
                            "user":cur[20]}
                                        
                dicq= """UPDATE celeb_stats SET P_m = %(P_m)s,
                                                P_h = %(P_h)s,
                                                P_l = %(P_l)s,
                                                P_um = %(P_um)s,
                                                P_uh = %(P_uh)s
                                            WHERE user = %(user)s """

                
                try:
                    self.sql.q(dicq,dicvals)
                    print("Success")
                except UnicodeEncodeError:
                    try:
                        print("UNIDECODE ERROR, trying decode...")
                        for k in dicvals:
                            dicvals[k] = unidecode(dicvals[k])
                        self.sql.q(dicq,dicvals)
                        succeeded = True
                    except:
                        print("Unidecode failed :(")


    def genStats(self, user_name):
        """
        Generates Twitter Statistics About a user & Pushes to MYSQL DB
        """

        #create SQL query to get all tweets from user
        q = "SELECT created_at,text FROM tweets WHERE from_user=%(user_name)s ORDER BY created_at"
        vals = {'user_name':user_name}
        tweets = self.sql.q(q,vals)

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
                           "user":user_name,
                           "ph":0
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
                           "user":user_name,
                           "ph":0
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
                                            %(user)s,
                                            %(ph)s,
                                            %(ph)s,
                                            %(ph)s,
                                            %(ph)s,
                                            %(ph)s,
                                            %(ph)s,
                                            %(ph)s,
                                            %(ph)s,
                                            %(ph)s)
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
                                            unique_mention=%(unique_mention)s,
                                            P_m=%(ph)s,
                                            P_h=%(ph)s,
                                            P_l=%(ph)s,
                                            P_um=%(ph)s,
                                            P_uh=%(ph)s,
                                            dim_1=%(ph)s,
                                            dim_2=%(ph)s,
                                            dim_3=%(ph)s,
                                            dim_4=%(ph)s """


        succeeded = False
        try:
            self.sql.q(dicq,dicvals)
            succeeded = True
            print ("Success")
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

    def createStatDB(self):
        #q = "SELECT * FROM celebs"
        #celebs = self.sql.q(q)

        #for celeb in celebs:
        #    self.genStats(celeb[0])


        q = "SELECT * FROM celeb_stats"
        celebs = self.sql.q(q)

        #self.genPercentileColumns(celebs)

        self.genPersonalityColumns(celebs)

    def deleteRows(self):
        query = "DELETE FROM celeb_stats"
        self.sql.q(query)

if __name__ == '__main__':
    tg = TweetStatGenerator()
    #tg.deleteRows()
    tg.createStatDB()
