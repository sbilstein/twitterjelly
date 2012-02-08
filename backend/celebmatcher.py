from dbsql import *
import sys

def getCelebMatches(userstats,celebstats):
    
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
        if celeb[0] == -1:
            continue

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

    pers =""
    if P_l > float(.5):
        pers += "S"
    else:
        pers += "C"

    if (P_m + P_um)/float(2.0) > float(.5):
        print (str(P_m+ P_um))
        pers += "W"
    else:
        pers += "T"

    if (P_h + P_uh)/float(2.0) > float(.5):
        pers += "J"
    else:
        pers += "M"

    #GO THROUGH LIST OF CELEBS AGAIN AND FIND THOSE WITH SAME PERSONALITY

    return [pers, listOfCelebs] 
