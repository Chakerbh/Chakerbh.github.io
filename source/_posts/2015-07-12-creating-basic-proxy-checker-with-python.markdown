---
layout: post
title: "Creating Basic Proxy Checker With Python"
date: 2015-07-12 11:03:54 +0100
comments: true
categories: Python security proxy
image:
  feature: /images/vim.jpg
---

I'm in love with web scrapping but sometimes I get banned by the site that I wanna extract the data from. So the first and basic solution is to use proxies. However finding a working proxy in a proxy list is pain in the neck. That's why I decided to create my own "basic" proxy checker.

<!-- more -->

## The idea: 
It's very simple, all we gonna do is to test our proxies:

1. Test connectivity.
2. Test timeout.
3. Check if the proxy is returning the right page or not.

## What I need:

* Python: DAHH!!!
* We gonna use [requests](http://docs.python-requests.org/en/latest/) module for the HTTP requests. If you don't already have it you should take a look. And if you don't wanna to install it you can simply follow on but you have to adapt the function to your library of choice.
* Proxy list to test. If you don't have one just google it.

## Check a single proxy:


First let's start by creating a function that test a single proxy. The function will load a webpage and return False if there are error during the request. Then check if the title is in the HTML or not and then return the result.

```python Check single proxy 
def checkproxy(proxy, timeout = 5, url="http://example.com", title="<title>Example Domain</title>"):
    proxies = {
            "http" : "http://" + proxy,
            "https" : "https://" +proxy
            } # Prepare the proxy
    try : # Try to make a GET Request to URL.
        r = requests.get(url,proxies=proxies, timeout=timeout)
    except : # If any error occured (Including timeout) return False.
        return False
    return title in r.text # Else check if title is in the HTML and return the result.
```
By default this function will try to connect to `http://example.com` with a timeout of `5` seconds. If every thing passed OK it will check the presence of `<title>Example Domain</title>` and return the result. 

OK Now we have a function that test if a given proxy is valid or not. But I wanna to check a proxy list? So we need to speed things up. Since checking every proxy aside will take time. We should try threads.

## Using threads:

Checking a proxy list with a single thread is very slow. But implementing threaded solution to this problem is not quite straightforward. So I do a little search and I found [this](http://stackoverflow.com/a/2635066/4237058). And with some modification I ended up with this:

{% gist e47e21aa36995783b690 %}


So I run it on on `6k` proxy list and It's reasonably fast. 

This script will print the valid proxy to `stdout`. But it should be no problem to redirect it to file or to modifie it to write it directly to a file. Feel free to modifie and/or to use the script. And don't forget to comment below.


