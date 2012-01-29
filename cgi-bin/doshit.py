
def DoSomeShit():
    tweettxts = DataGrabber().GetAllText()
    sql = SQLQuery()
    corpus = TfIdf()

    count = 0
    vals = {}
    q =  "INSERT IGNORE INTO tokens (token, type) VALUES"
    
    for txt in tweettxts:
        topstart = time.time()
        #print(txt)
        tokens = corpus.get_tokens(txt[0])
        #count = 0
        #vals = {}
        #q =  "INSERT IGNORE INTO tokens (token, type) VALUES"
        for token in tokens:
            print(token)
            vals['token'+str(count)] = token[0]
            vals['type'+str(count)] = token[1]
            q += "(%(token"+str(count)+")s, %(type"+str(count)+")s),"
            count += 1

        print("txt took ",time.time() - topstart)
        
    q = q[:len(q)-1]
    #print(q)
    #print(q%vals)
    print("querying...")
    start = time.time()
    sql.q(q,vals)
    print("query took ",time.time() - start)

def DoSomeOtherShit():
    sql = SQLQuery()
    q = """SELECT tfidf.token, tfidf.c2/tfidf.c as score FROM
              (SELECT token, SUM(CASE WHEN user="%(user)s" THEN 1 ELSE 0 END) AS c2, COUNT(*) AS c FROM
                    token_user_mapping GROUP BY token ORDER BY c DESC)
              as tfidf WHERE tfidf.c2 != 0
            ORDER BY score DESC"""

    users = pickle.load(open('topusers.pkl','rb'))
    for user in users:
        print(user)
        vals = {'user':user}
        print(q%vals)
        userdata = sql.q(q%vals)
        debuglog.pprint_msg(userdata)

    def GetCelebTFIDFs(self, terms):
        q = "SELECT COUNT(DISTINCT tweets.from_user) FROM tweets";
        result = self.sql.q(q)
        totalcelebs = result[0][0]
        print(totalcelebs)
        
        q = """SELECT token_counts.*, COUNT(token_user_mapping.user) as total_user_tokens FROM (SELECT t.c, t.user
                FROM (SELECT user, COUNT(*) as c
                    FROM token_user_mapping WHERE token=%(term)s GROUP BY user) as t
                 ORDER BY t.user) as token_counts, token_user_mapping
WHERE token_user_mapping.user = token_counts.user GROUP BY token_user_mapping.user"""

        vals = {'term':term}
        results = self.sql.q(q,vals)
        celebswithterm = len(results)
        celebscores = {}
        for result in results:
            celeb = result[1]
            total_tokens_for_celeb = result[2]
            term_count_for_celeb = result[0]          
            
            celebscores[celeb] = float(term_count_for_celeb)/float(total_tokens_for_celeb) * float(totalcelebs)/float(celebswithterm)

        return celebscores
