from _ctypes_test import func
from functools import wraps
import time
import debuglog

def perftest(func):
    """A decorator that prints the time a function takes to execute."""
    @wraps(func)
    def wrapper(*args, **kw):
        start_time = time.time()
        value = func(*args, **kw)
        debuglog.msg("\nPERFTEST===============\nFunction:\t%s\nTime:\t%s\n"%
                     (func.__module__ + "::" + func.__name__, str(time.time() - start_time)), mode="debug")

        return value
        # Now a few lines needed to make simple_decorator itself
    return wrapper