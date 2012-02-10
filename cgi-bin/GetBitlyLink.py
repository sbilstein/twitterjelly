#!C:\Python32\python.exe
__author__ = 'jonathan'

import cgi
import json
import bitly_api

print("Content-Type: application/json\n")

form = cgi.FieldStorage()

if "url" in form:
    c = bitly_api.Connection('lemurturtle','R_34fc9204f01e52ec3ed11a4f4a71fac1')
    print(json.dumps(c.shorten(form["url"].value)))
else:
    print(json.dumps({'status':'error'}))