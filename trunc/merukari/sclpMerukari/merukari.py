# -*- coding: utf-8 -*-
import sys
import os
import glob
import pandas
import time
import datetime
import random
import string
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../lib')
from const import *
from utility import *
from bs4 import BeautifulSoup

############################
###### Function       ######
############################
def getSeriesFromItemsbox(url, price):
    # Load URL to browser
    browser2.get(url)
    
    ##  Save Html files just in case
    itemID = url.replace(stringBaseUrl, '').split('/')
    soup = BeautifulSoup(browser2.page_source, 'html.parser')
    saveHtmlFile(soup, stringPathToTmpHtml + dataSetName + "/", itemID[0] + ".html")

    # Get title
    title = getText_find_element_by_css_selector(browser2, stringItemName)

    # Get URL
    pageUrl = url[:url.rfind('?')-1]

    # Get Owner
    trs = browser2.find_element_by_class_name(stringItemDetailTable).find_elements_by_css_selector("tr")
    for tr in trs:
        strTh = getText_find_element_by_css_selector(tr,"th")
        if (strTh == stringOwner_Utf8):
            owner = getText_find_element_by_css_selector(tr,"td a")

    isSold = 0
    if len(getText_find_element_by_css_selector(browser2, stringItemSoldOutBadge)) > 0:
        isSold = 1

    # Get sub category and sub-sub category
    sub_category     = getText_find_element_by_css_selector(browser2, stringItemDetailTableSubCategory)
    sub_sub_category = getText_find_element_by_css_selector(browser2, stringItemDetailTableSubSubCategory)

    # Get brand name
    trs = browser2.find_element_by_class_name("item-box-container").find_elements_by_css_selector("tr")
    for tr in trs:
        strTh = getText_find_element_by_css_selector(tr,"th")
        if (strTh == stringBrand_Utf8):
            brand = getText_find_element_by_css_selector(tr,"td")
    # Get imgUrl
    imgUrl = browser2.find_element_by_class_name("owl-item-inner").find_element_by_class_name("owl-lazy").get_attribute("data-src")
    timestamp = getItemTimeStamp(imgUrl)
    se = pandas.Series([title,price,isSold,pageUrl,sub_category,sub_sub_category,brand,owner,imgUrl],
                       ['title','price','sold','url','sub_category','sub_sub_category','brand','owner','imgUrl'])
    se.str.encode(encoding="utf-8")
    return se

def getItemTimeStamp(url):
    r = requests.get(url)
    resJson = r.headers
    loadedJson = json.load(resJson)
    timestamp = loadedJson["Last-Modified"]
    print(timestamp)
    return timestamp

def getSeriesFromItemsboxFromLocalDirectory(url):
    # Load URL to browser
    browser2.get(url)

    # Get title
    title = getText_find_element_by_css_selector(browser2, stringItemName)

    # Get URL
    pageUrl = stringBaseUrl + url[url.rfind('/')+1:]
    pageUrl = pageUrl.replace(".html","")

    # Get price
    price = getText_find_element_by_css_selector(browser2, stringItemPrice)
    price = price.replace("¥ ", "").replace(",", "")

    # Get Owner
    trs = browser2.find_element_by_class_name(stringItemDetailTable).find_elements_by_css_selector("tr")
    for tr in trs:
        strTh = getText_find_element_by_css_selector(tr,"th")
        if (strTh == stringOwner_Utf8):
            owner = getText_find_element_by_css_selector(tr,"td a")

    isSold = 0
    if len(getText_find_element_by_css_selector(browser2, stringItemSoldOutBadge)) > 0:
        isSold = 1

    # Get sub category and sub-sub category
    sub_category     = getText_find_element_by_css_selector(browser2, stringItemDetailTableSubCategory)
    sub_sub_category = getText_find_element_by_css_selector(browser2, stringItemDetailTableSubSubCategory)

    # Get brand name
    trs = browser2.find_element_by_class_name("item-box-container").find_elements_by_css_selector("tr")
    for tr in trs:
        strTh = getText_find_element_by_css_selector(tr,"th")
        if (strTh == stringBrand_Utf8):
            brand = getText_find_element_by_css_selector(tr,"td")

    se = pandas.Series([title,price,isSold,pageUrl,sub_category,sub_sub_category,brand,owner],
                       ['title','price','sold','url','sub_category','sub_sub_category','brand','owner'])
    se.str.encode(encoding="utf-8")
    return se

def getDescriptionTextFromItemsbox(url):
    # Load URL to browser
    browser2.get(url)

    # Get item desctiption
    des = getText_find_element_by_css_selector(browser2, "p.item-description-inner")
    return des

# Scraping from local directory
def scrapingFromLocalDirectory(directoryPath, df):
    tmpHtmlList = sorted(
        glob.glob(directoryPath), key=os.path.getmtime)

    for tmpHtml in tmpHtmlList:
        tmp = "file:///" + os.getcwd() + "/" + tmpHtml
        se = getSeriesFromItemsboxFromLocalDirectory(tmp)
        df = df.append(se, ignore_index=True)
    return df

# scraping pages, paramter is URL
def scrapelToGetDescription(num_page, url):
    browser1.get(url)
    page = 1
    des = ""
    while page != num_page:
        if len(browser1.find_elements_by_css_selector(stringNextPage)) > 0:
            print("######################page: {} ########################".format(page))
            print("Starting to get posts...")

            posts = browser1.find_elements_by_css_selector(".items-box")
            # Get next page url
            btn = browser1.find_element_by_css_selector(
                "li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")

            for post in posts:
                url = post.find_element_by_css_selector("a").get_attribute("href")
                des += getDescriptionTextFromItemsbox(url)

            # Increment page number
            page+=1

            print("Next url:{}".format(btn))
            browser1.get(btn)
            print("Moving to next page......")

        # There isn't next page
        else:
            print("no pager exist anymore")
            break
    return des

# Crowling pages, paramter is URL
def crowling(num_page, url, df):
    browser1.get(url)
    page = 1
    while page != num_page:
        if len(browser1.find_elements_by_css_selector(stringNextPage)) > 0:
            print("######################page: {} ########################".format(page))
            print("Starting to get posts...")

            posts = browser1.find_elements_by_css_selector(".items-box")
            # Get next page url
            btn = browser1.find_element_by_css_selector(
                "li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")

            for post in posts:
                url = post.find_element_by_css_selector("a").get_attribute("href")

                ## Scraping without tmp html
                priceBox = getText_find_element_by_css_selector(post, ".items-box-price")
                priceBox = priceBox.replace("¥ ", "").replace(",", "")

                se = getSeriesFromItemsbox(url, priceBox)
                df = df.append(se, ignore_index=True)

            # Increment page number
            page+=1

            print("Next url:{}".format(btn))
            browser1.get(btn)
            print("Moving to next page......")

        # There isn't next page
        else:
            print("no pager exist anymore")
            break

    return df

############################
###### Process        ######
############################
# Get parameter from command line
args = sys.argv
argc = len(args)
# Check parameter
if (argc <  2):
    print ('Usage: # python %s keyword_to_serch' % args[0])
    quit()

# Get date
today = datetime.date.today()

# Initialize browser
options = Options()
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--headless')

browser1 = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
browser2 = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
#browser1 = webdriver.Chrome(chrome_options=options, executable_path='C:\DRIVER\webdriver\chromedriver.exe')
#browser2 = webdriver.Chrome(chrome_options=options, executable_path='C:\DRIVER\webdriver\chromedriver.exe')

query = args[1]
dataSetName = "{0}_{1}".format(query, today)

# Create tmp directory date + query
if os.path.isdir(stringPathToTmpHtml + dataSetName) != True:
    os.mkdir(stringPathToTmpHtml + dataSetName)

# Get URL, Setting of serch setting
webUrl = (stringMerikariUrl + stringSerch +
 "?" + stringSortOrder +            "=" + stringCreatedDesc +  # Sort
 "&" + stringCategoryRoot +         "=" + "2"               +  # root category 1=lady's 2=men's
 "&" + stringStatusTradingSoldOut + "=" + "1"               +  # Status "sold out"
#"&" + stringStatusOnSale +         "=" + "1" +                # Status "On sale"
 "&" + stringPriceMin +             "=" + stingPriceMinValue + # Minimum price
 "&" + stringItemStatus +           "=" + "1"               +  # Status of Item
 "&" + stringKeyword +              "=" + "{}".format(query))  # Keyword

if (argc == 3):
    if (args[2] == "--scrape"):
        # Scraping
        print("Option: --scrape")
        df = pandas.read_csv(stringCsvFileName, index_col=0)
        df = scrapingFromLocalDirectory(stringPathToTmpHtml + dataSetName + "/*", df=df)
        df.to_csv(stringPathToDatum + dataSetName + ".csv", encoding="utf-8", sep='\t')

    elif (args[2] == "--getdtl"):
        # Get item detail
        print("Option: --getdtl")
        text = scrapelToGetDescription(num_page=20, url=webUrl)
        with open(stringPathToDatum + dataSetName + ".txt", 'ab') as f:
            f.write(text.encode('utf-8', 'ignore'))

    else:
        print("invalid option")
else:
    # Continue to crowling until specified page
    print("Option: default")
    # Read csv file
    df = pandas.read_csv(stringCsvFileName, index_col=0)
    df = crowling(num_page=20, url=webUrl, df=df)
    df.to_csv(stringPathToDatum + dataSetName + ".csv", encoding="utf-8", sep='\t')

# Close browser
browser1.quit()
browser2.quit()

# Return csv file name
sys.exit(dataSetName + ".csv")
