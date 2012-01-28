#!/usr/bin/env python

import pymysql

#conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql')

conn = pymysql.connect(host='66.147.244.176', port=3306, user='sbilstei_default', passwd='db$wag', db='sbilstei_twitter')
   

cur = conn.cursor()

cur.execute("""SELECT id FROM tweets""")

# print cur.description

# r = cur.fetchall()
# print r
# ...or...
ids = []
print(cur.fetchall())
for r in cur.fetchall():
   print(r[0])
   ids.append(r[0])
print(ids)
cur.close()
conn.close()
