from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.error import URLError
from bs4 import BeautifulSoup

def getTitle(url):
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
        title = bsObj.body.h1
    except AttributeError as e:
        print(e)
        return None
    return title

title = getTitle("http://www.pythonscraping.com/pages/page1.html")
if title == None:
    print("Title could not be found\n")
else:
    print(title)
