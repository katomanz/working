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
            return bsObj.findAll("a", {"class":"a-link-normal"}, target="_blank")
    except AttributeError as e:
        print(e)
        return None
    return title

url = "https://www.amazon.co.jp/gp/bestsellers/books"
# To get title of commodity from amazon
titleList = getRequestTag(url, 1)

if titleList == None:
    print("Name list could not be found\n")
else:
    for title in titleList:
        print(title.get_text())
#        print(title.parent)

searchHtml = urlopen("https://www.mercari.com/jp/search/?keyword=")
searchObj = BeautifulSoup(searchHtml.read(),"lxml")
print(searchObj.find("span", {"itemprop":"title"}).get_text())
