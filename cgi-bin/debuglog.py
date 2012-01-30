__author__ = 'jonathan'

import pprint

def msg(*args, mode="debug"):
    if mode == "debug":
        print(*args)
    elif mode =="server":
        print(*args, file=open("./debug.log", "a"))

def pprint_msg(obj, mode="debug"):
    if mode == "debug":
        pprint.pprint(obj)
    elif mode == "server":
        print(pprint.pformat(obj), file=open("./debug.log", "a"))