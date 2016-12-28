from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

def getRequestTag(url, tag):
    try:
        html = urlopen(url)
    except HTTPError as e:
        print(e)
        return None
    except URLError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(),"lxml")
        if tag == 0:
            return bsObj.body.h1
        elif tag == 1:
            return bsObj.findAll("span", {"class":"green"})
    except AttributeError as e:
        print(e)
        return None
    return title

url = "http://www.pythonscraping.com/pages/warandpeace.html"
namelist = getRequestTag(url, 1)
title = getRequestTag(url, 0)

if namelist == None:
    print("Name list could not be found\n")
else:
    for name in namelist:
        print(name.get_text())

if title == None:
    print("Title could not be found\n")
else:
    print(title)
