import urllib.request
import urllib.parse
import json
import pprint
import re
from tfidf import *

twitterquery = "from:justinbieber"
twitterquery = urllib.parse.quote(twitterquery)
print(twitterquery)
queryurl = "http://search.twitter.com/search.json?q=%s"%twitterquery
print(queryurl)
data = json.loads(urllib.request.urlopen(queryurl).read().decode("ascii"))

debuglog.pprint_msg(data)

corpus = TfIdf()
tweets = []                                                                                                                           
for tweet in data['results']:
    text = tweet['text']
    tweets.append(text)
    corpus.add_input_document(text)
    print(corpus.get_num_docs())

for tweet in tweets:
    debuglog.pprint_msg(corpus.get_doc_keywords(tweet))


    
    
