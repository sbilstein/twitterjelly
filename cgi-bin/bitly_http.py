"""
This class is an abstracted http handler that uses multiple underlying http libraries 

it will default to
a) google urlfetch
b) pycurl
c) urllib2

"""
try:
    import pycurl
    PYCURL = True
except ImportError:
    PYCURL = False

import urllib.request, urllib.error, urllib.parse
import io

class DontRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if code in (301, 302, 303, 307):
            raise urllib.error.HTTPError(req.get_full_url(), code, msg, headers, fp)

def makeUrllib2Http(url, user_agent):
    dont_redirect = DontRedirect()
    opener = urllib.request.build_opener(dont_redirect)
    opener.addheaders = [('User-agent', user_agent + ' urllib')]

    try:
        response = opener.open(url)
        code = response.code
        data = response.read()
    except urllib.error.URLError as e:
        return 500, str(e)
    except urllib.error.HTTPError as e:
        code = e.code
        data = e.read()
    return code, data

def makePycurlHttp(url, timeout, user_agent):
    try:
        buffer = io.StringIO()

        curl = pycurl.Curl()
        curl.setopt(pycurl.TIMEOUT_MS, timeout)
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.FOLLOWLOCATION, 0)
        curl.setopt(pycurl.MAXREDIRS, 0)
        curl.setopt(pycurl.WRITEFUNCTION, buffer.write)
        curl.setopt(pycurl.NOSIGNAL, 1)
        curl.setopt(pycurl.USERAGENT, user_agent + ' ' + pycurl.version)
        # if referer:
        #     curl.setopt(pycurl.REFERER, referer)

        curl.perform()
        result = buffer.getvalue()
        buffer.close()
        http_status_code = curl.getinfo(pycurl.HTTP_CODE)
        curl.close()
    except:
        try:
            curl.close()
        except:
            pass
        raise
    return http_status_code, result

def get(url, timeout, user_agent):
    if PYCURL:
        code, result = makePycurlHttp(url, timeout, user_agent)
    else:
        code, result = makeUrllib2Http(url, user_agent)
    return {'http_status_code':code, 'result':result}
