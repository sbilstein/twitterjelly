#!c:/Python32/python.exe
__author__ = 'jonathan'

import cgi
from datagrabber import *
import json
#import cgitb
#cgitb.enable(display=0, logdir="./log")

print("Content-Type: application/json\n")

form = cgi.FieldStorage()

if "user" not in form:
    print(json.dumps({ 'status': 'error'}))
else:
    user = form['user'].value
    if user is None or not len(user) or len(user) > 20 or user.count(' '):
        print(json.dumps({ 'status': 'error'}))
    else:
        print(json.dumps(DataGrabber().GetCelebMatchesForUser(user)))

