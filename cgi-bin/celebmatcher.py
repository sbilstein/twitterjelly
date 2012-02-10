from dbsql import *
import sys
import tweetadder
import datetime
import math
import collections
import pprint
import random
import debuglog

def getCelebMatches(userdata, celebstats):
    #FIRST CALCULATE BASE STATS FOR USER
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
        userstats ={}
        if total_tweets != 0:
            userstats = {"tr_day": float(total_tweets)/num_days,
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

    #calculate percentile stats for user    
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
        
    for celeb in celebstats:
        #counts for percentiles
        N += 1
        if celeb[14] < userstats["mention_rate"]:
            B_m += 1
        elif celeb[14] == userstats["mention_rate"]:
            E_m += 1

        if celeb[16] < userstats["hash_rate"]:
            B_h += 1
        elif celeb[16] == userstats["hash_rate"]:
            E_h += 1

        if celeb[17] < userstats["link_rate"]:
            B_l += 1
        elif celeb[17] == userstats["link_rate"]:
            E_l += 1

        if celeb[18] < userstats["unique_hash"]:
            B_uh += 1
        elif celeb[18] == userstats["unique_hash"]:
            E_uh += 1

        if celeb[19] < userstats["unique_mention"]:
            B_um += 1
        elif celeb[19] == userstats["unique_mention"]:
            E_um += 1

    #CALCULATE PERCENTILES
    P_m = ((B_m + 0.5*E_m)/N)*100
    P_h = ((B_h + 0.5*E_h)/N)*100
    P_l = ((B_l + 0.5*E_l)/N)*100
    P_um = ((B_um + 0.5*E_um)/N)*100
    P_uh = ((B_uh + 0.5*E_uh)/N)*100

    #use all info about user to get personality
    if P_l > float(50.0):
        dim_2 = "S"
    else:
        debuglog.msg(P_l)
        dim_2 = "C"

    if (P_m + P_um)/float(2.0) > float(50.0):
        dim_3 = "W"
    else:
        dim_3 = "T"

    if (P_h + P_uh)/float(2.0) > float(50.0):
        dim_4 = "J"
    else:
        dim_4 = "M"



    #get average tweet rates
    m_fri = sum([userstats["tr_monday"],userstats["tr_tuesday"],userstats["tr_wednesday"],userstats["tr_thursday"],userstats["tr_friday"]])/5.0
    sa_su = sum([userstats["tr_saturday"],userstats["tr_sunday"]])/2.0
    day = sum([userstats["tr_morning"],userstats["tr_afternoon"]])/2.0
    night = sum([userstats["tr_earlymorning"],userstats["tr_latenight"],userstats["tr_evening"],userstats["tr_night"]])/4.0

    #avg tweet rate on time off
    tr_weekend = (sa_su + night)/2.0
    tr_weekday = ((m_fri + day)/2.0)*1.3

    if tr_weekday > tr_weekend:
        dim_1 = "A"
    else:
        dim_1 = "E"

    #GO THROUGH LIST OF CELEBS AGAIN AND FIND THOSE WITH SAME PERSONALITY
    matches = []

    for celeb in celebstats:
        if celeb[26]==dim_1 and celeb[27]==dim_2 and celeb[28]==dim_3 and celeb[29]==dim_4:
            matches.append(celeb[20])

    toreturn=[dim_1+dim_2+dim_3+dim_4]
    random.shuffle(matches)
    if len(matches) > 24:
        toreturn.append(matches[0:24])
    else:
        toreturn.append(matches[0:len(matches)])
        
    
    return toreturn
