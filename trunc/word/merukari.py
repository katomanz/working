# -*- coding: utf-8 -*-
import sys
import os
import glob
import time
import datetime
import random
import string
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

############################
###### Strings        ######
############################
# URL sting
stringMerikariUrl="https://www.mercari.com/jp/"
stringSerch="search/"

# Path to Datum
stringPathToDatum="./datum/"

# Path to tmpHtml
stringPathToTmpHtml="./sclpMerukari/tmpHtml/"

# Identifer for sort
stringSortOrder="sort_order"
stringCreatedDesc="created_desc"

# Flag identifer if sold out or not
stringStatusTradingSoldOut="status_trading_sold_out"
stringStatusOnSale="status_on_sale"

# Identifer for minimum price and value
stringPriceMin="price_min"
stingPriceMinValue="3000"

stringItemStatus="item_condition_id[1]"

# Identifer for keyword
stringKeyword="keyword"

# Identifer for root category
stringCategoryRoot="category_root"

# format of csv file
stringCsvFileName="./sclpMerukari/default.csv"

# string for brand utf-8
stringBrand_Utf8=u"ブランド"

# string for owner utf-8
stringOwner_Utf8=u"出品者"

# string for mercari base URL
stringBaseUrl="https://item.mercari.com/jp/"

# string for next page
stringNextPage="li.pager-next .pager-cell:nth-child(1) a"

############################
###### Function       ######
############################
def getText_find_element_by_css_selector(browser, cssSel):
    try:
        ret = browser.find_element_by_css_selector(cssSel).text
    except:
        print("Could not find " + cssSel)
        ret = "NA"
    finally:
        return ret

def getDescriptionTextFromItemsbox(url):
    # Load URL to browser
    browser2.get(url)

    # Get item desctiption
    des = getText_find_element_by_css_selector(browser2, "p.item-description-inner")
    return des

# Get Html file only
def getHtmlFromItemsbox(url):
    browser2.get(url)
    return BeautifulSoup(browser2.page_source, 'html.parser')

# Crowling pages, paramter is URL
def crowlToGetDescription(num_page, url):
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

############################
###### Process        ######
############################
# Get parameter from command line
args = sys.argv
argc = len(args)
# Check parameter
if (argc != 2):
    print ('Usage: # python %s keyword_to_serch' % args[0])
    quit()

# Get date
today = datetime.date.today()

## For Linux Enviroment
#browser1 = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
#browser2 = webdriver.Chrome(executable_path='/usr/bin/chromedriver')

browser1 = webdriver.Chrome(executable_path='C:\DRIVER\webdriver\chromedriver.exe')
browser2 = webdriver.Chrome(executable_path='C:\DRIVER\webdriver\chromedriver.exe')

query = args[1]

dataSetName = "{0}_{1}".format(query, today)

# Get URL, Setting of serch setting
webUrl = (stringMerikariUrl + stringSerch +
 "?" + stringSortOrder +            "=" + stringCreatedDesc +  # Sort
 "&" + stringCategoryRoot +         "=" + "2"               +  # root category 1=lady's 2=men's
 "&" + stringStatusTradingSoldOut + "=" + "1"               +  # Status "sold out"
#"&" + stringStatusOnSale +         "=" + "1" +                # Status "On sale"
 "&" + stringPriceMin +             "=" + stingPriceMinValue + # Minimum price
 "&" + stringItemStatus +           "=" + "1"               +  # Status of Item
 "&" + stringKeyword +              "=" + "{}".format(query))  # Keyword

# Continue to crowling until specified page
description = crowlToGetDescription(num_page=20, url=webUrl)

# Create tmp directory date + query
if os.path.isdir(stringPathToDatum) != True:
    os.mkdir(stringPathToDatum)

with open(stringPathToDatum + dataSetName + ".txt", 'ab') as f:
    f.write(description.encode('cp932', 'ignore'))

# Close browser
browser1.quit()
browser2.quit()

# Return csv file name
sys.exit(dataSetName + ".txt")
