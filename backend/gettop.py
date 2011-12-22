import urllib.request
import re
import pprint
import pickle

numpages = 20
urls = ["http://twittercounter.com/pages/100"]

for i in range(1,numpages):
    print(i)
    urls.append("http://twittercounter.com/pages/100/%s"%str(20*i))

pprint.pprint(urls)

usernames = []
for url in urls:
    print("fetchting",url)
    page = urllib.request.urlopen(url).read().decode("utf-8")
    usernames.extend(re.findall("\(@(\w*?)\)",page))

print(usernames)
print(len(usernames))
f = open("topusers.pkl",'wb')
pickle.dump(usernames, f)
f.close()
