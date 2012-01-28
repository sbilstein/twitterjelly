from dbsql import *

class TFIDFTableGenerator:
    '''Generates table of TFIDF scores by word for each celeb'''

    def __init__(self):
        self.sql = SQLQuery()

    def Generate(self):
        self.GenerateDocFreqsTable()

        celeb_count = self.GetCelebCount()

        tokens = self.GetTokens()
        
        q = """SELECT token_counts.user, token_counts.c, COUNT(token_user_mapping.user) as total_user_tokens
                  FROM
                    (SELECT t.user, t.token, t.c
                      FROM
                        (SELECT user, token, COUNT(*) as c
                          FROM token_user_mapping
                          WHERE token=%(token)s
                          GROUP BY user) as t
                        ORDER BY t.user) as token_counts, token_user_mapping
                  WHERE token_user_mapping.user = token_counts.user GROUP BY token_user_mapping.user"""

        #ITERATE THROUGH TOKENS
        for token in tokens:
            if len(token) < 3:
                print("token %s too short."%token)
                continue;
            elif token[0] == '@':
                print("ignoring user token %s"%token)
                continue;
            
            print("Generating tfidf table for token <%s>"%token)
            vals = {'token':token}
            results = self.sql.q(q, vals)

            if results is None:
                continue;
            
            #CALCULATE SCORES
            celebs_with_term = len(results)
            celeb_scores = {}
            for result in results:
                celeb = result[0]
                term_count_for_celeb = result[1]
                total_tokens_for_celeb = result[2]
                celeb_tfidf_for_term = float(term_count_for_celeb) / float(total_tokens_for_celeb) * float(celeb_count)/float(celebs_with_term)
                celeb_scores[celeb] = (celeb_tfidf_for_term, term_count_for_celeb)

            #GENERATE QUERY
            insert_q = "INSERT INTO celeb_tfidf (user, token, score, count) VALUES"

            count = 0
            vals = {'token':token}
            
            for celeb in celeb_scores:
                vals['celeb'+str(count)] = celeb
                vals['score'+str(count)] = str(celeb_scores[celeb][0])
                vals['count'+str(count)] = str(celeb_scores[celeb][1])
                insert_q+= "(%(celeb"+str(count)+")s, %(token)s, %(score"+str(count)+")s, %(count"+str(count)+")s),"
                count += 1

            #remove last comma and encode
            insert_q = insert_q[:len(insert_q)-1]

            #pprint.pprint(vals)
            
            #EXECUTE QUERY
            self.sql.q(insert_q,vals)     

            

    def GenerateDocFreqsTable(self):
        '''to do: just update the frequencies as data is read in instead of generating this table.'''
        q = "DROP TABLE doc_freqs;"

        self.sql.q(q)

        q = """CREATE TABLE doc_freqs
                  SELECT num_users_with_term.token, COUNT(*) as c
                    FROM
                      (SELECT DISTINCT token, user
                        FROM token_user_mapping as users_with_term
                        ORDER BY token) as num_users_with_term
                    GROUP BY num_users_with_term.token
                    ORDER BY c DESC;"""
        self.sql.q(q)

    def GetCelebCount(self):
        q = "SELECT COUNT(DISTINCT tweets.from_user) FROM tweets";
        result = self.sql.q(q)
        totalcelebs = result[0][0]

        return totalcelebs

    def GetTokens(self):
        celeb_count = self.GetCelebCount();
        q = "SELECT token FROM tokens WHERE tokens.type != 'user'"
        tokens = self.sql.q(q)
        return [t[0] for t in tokens]

if __name__ == '__main__':
    TFIDFTableGenerator().Generate()
            
        
