__author__ = 'jonathan'

import pprint

def msg(*args, mode="server"):
    if mode == "debug":
        print(*args)
    elif mode =="server":
        print(*args, file=open("../../log/debug.log", "a"))

def pprint_msg(obj, mode="server"):
    if mode == "debug":
        pprint.pprint(obj)
    elif mode == "server":
        print(pprint.pformat(obj), file=open("../../log/debug.log", "a"))
