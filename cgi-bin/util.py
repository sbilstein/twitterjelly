from _ctypes_test import func
from functools import wraps
import time
import debuglog
import urllib.request

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

# create a password manager
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

# Add the username and password.
# If we knew the realm, we could use it instead of None.
top_level_url = "http://50.56.221.228/"
password_mgr.add_password(None, top_level_url, "twitter", "jelly")

handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

# create "opener" (OpenerDirector instance)
opener = urllib.request.build_opener(handler)

# use the opener to fetch a URL
opener.open("http://50.56.221.228/cgi-bin/idf.php")

# Install the opener.
# Now all calls to urllib.request.urlopen use our opener.
urllib.request.install_opener(opener)