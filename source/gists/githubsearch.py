import requests
import re

def search_api_keys(keyword, keyregex):
    numberOfKey = 0
    with open(keyword+".txt", "a") as f:
        base ="https://raw.githubusercontent.com"
        l = requests.get("https://github.com/search?q={}&type=Code&ref=searchresults".format(keyword))
        for language in re.findall('<a href="(.*?)".*?ter-item">',l.text):
            for page in range(1,100):
                req = requests.get(language + "&p={}".format(page))
                for url in  re.findall('a href="(.*?)" title', req.text):
                    raw = base + url.replace("/blob", "")
                    r = requests.get(raw)
                    apikey =  re.findall(keyregex, r.text, re.I)
                    if apikey != []:
                        f.write(apikey[0]+"\n")
                        numberOfKey +=1
        print numberOfKey + "Keys has been found"        


rotten = "rottentomatoes+api"
rottenregex = "api[-_]?key.*?['\"]+(.{24})['\"]"
#search_api_keys(rotten, rottenregex)


twitter = "consumer_key+twitte"
twitterregex = '(sumer|ken).*?=.*?(\'|")(.{20,50}?)(\'|")'
#search_api_keys(twitter, twitterregex)

tmdb = "tmdb+api"
tmdbregex = "((api[-_.]?key)|api).*?[ ='\"\(]*(.*?)['\"\)]*$"
#search_api_keys(tmdb, tmdbregex)

google = "AIza+api"
googleregex = "(AIza.{35})"
search_api_keys(google, googleregex)

