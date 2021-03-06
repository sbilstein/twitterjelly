#!C:\Python32\python.exe
__author__ = 'jonathan'

import cgi
from dbsql import *
import json

print("Content-Type: application/json\n")

form = cgi.FieldStorage()

if "id" in form and len(form["id"].value) == 32 and not form["id"].value.count(' '):
    q = "SELECT json FROM stored_matches_json WHERE hashed=%(hash)s"
    vals = {'hash':form["id"].value}
    if "user" in form and len(form["user"].value) < 20 and not form["user"].value.count(' '):
        q += " AND user=%(user)s"
        vals["user"] = form["user"].value

    results = SQLQuery().q(q, vals)
    if results and len(results):
        jresults = json.loads(results[0][0])
        jresults["permalink_id"] = form["id"].value
        print(json.dumps(jresults))
    else:
        print(json.dumps({'status':'error'}))
else:
    print(json.dumps({'status':'error', 'error':'invalid_permalink'}))

