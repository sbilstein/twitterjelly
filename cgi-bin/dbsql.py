import pymysql
import pprint
import traceback
import sys
import debuglog
from util import *

class SQLQuery:
    @perftest
    def __init__(self):
        #self.conn = pymysql.connect(host='66.147.244.176', port=3306, user='sbilstei_default', passwd='db$wag', db='sbilstei_twitter')
        self.conn = pymysql.connect(host='50.56.221.228', port=3306, user='default_swag', passwd='db$wag', db='tjelly')
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def q(self, query, values=None, auto_str=True):
        try:
            if not values:
                self.cur.execute(query)
            else:
                self.cur.execute(query, values)
            self.conn.commit()
            return self.cur.fetchall()
        except:
            print("Query failed!")
            print("Query:",query)
            if values is not None:
                print("Vals:")
                debuglog.pprint_msg(values)
            traceback.print_exc(file=sys.stdout)
            exit

    
