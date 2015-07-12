---
layout: post
title: "Searching for APIs keys in github with python"
date: 2015-07-09 01:16:25 +0100
comments: true
categories: python github API security 
image:
  feature: /images/vim.jpg
---
I was inspired by the this post ["Automatically Enumerating Google API Keys from Github Search"](http://raidersec.blogspot.com/2013/03/automatically-enumerating-google-api.html) by [Jordan Wright](http://jordan-wright.com/) the creator of [dumpmon](https://github.com/jordan-wright/dumpmon). In which he discuss how to "harvest" google api key from github.

<!-- more -->

How it works?

The `searchApiKey` function expect two parameters `keyword` and `regex`. 
```python
    def searchApiKey(keyword, regex)
```

It use the `keyword` to search in Github. Then go through all 100 pages.

```python
req = requests.get("https://github.com/search?p={}&q={}&type=Code&ref=searchresults".format(i, keyword))
```

Here I run into problem since the code is formated in HTML so the regex won't work properly . 
{% img /images/googleapikey.png "Github html code" %}

For that I decided to fetch the url of every code snippet.


```python
for url in  re.findall('a href="(.*?)" title', req.text)
```

Then transform it into the raw url. That we can apply the regex on it.
```python
raw = base + url.replace("/blob", "")
```
That's all now all we need is to prepare the regex and call the function. Here some regex that I used them.

```python
#couple of regexes:

rotten = "rottentomatoes+api"
rottenregex = "api[-_]?key.*?['\"]+(.{24})['\"]"
#search_api_keys(rotten, rottenregex)


twitter = "consumer_key+twitte"
twitterregex = '(sumer|ken).*?=.*?(\'|")(.{20,50}?)(\'|")'    # Need some work 
#search_api_keys(twitter, twitterregex)

google = "AIza+api"
googleregex = "(AIza.{35})"
#search_api_keys(google, googleregex)

tmdb = "tmdb+api"
tmdbregex = "((api[-_.]?key)|api).*?[ ='\"\(]*(.*?)['\"\)]*$" # Need a lot of work
#search_api_keys(tmdb, tmdbregex)

```

For now this function will only get 10\*100 results, But we can improve this. Github offer the possibility to search by language. So we can search for every programming language apart. This offer 10 time more results to try our regex (sometimes less it depends on the keyword). Jordan Wright discuss in his blog another way to get more results( you can check them [here](http://raidersec.blogspot.com/2013/03/automatically-enumerating-google-api.html)). For me this is OK for now

Final result
{% gist bbe2eabb0a7e33bf0c89 %}


But why you didn't simply use Github API

Indeed Github is offering search in the API, But when I checked the [documentaion](https://developer.github.com/v3/search/) I found out that you can only search for code inside specific repository. And that doesn't help us at all.

```
"message": "Validation Failed",
"errors": [
{
      "message": "Must include at least one user, organization, or repository",
      "resource": "Search",
      "field": "q",
      "code": "invalid"
```

