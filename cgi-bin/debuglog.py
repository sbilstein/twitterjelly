__author__ = 'jonathan'

import pprint

default_mode = open('config.txt', 'r').read()

def msg(*args, mode=default_mode):
    if mode == "debug":
        print(*args)
    elif mode =="server":
        print(*args, file=open("../../logs/debug.log", "a"))

def pprint_msg(obj, mode=default_mode):
    if mode == "debug":
        pprint.pprint(obj)
    elif mode == "server":
        print(pprint.pformat(obj), file=open("../../logs/debug.log", "a"))