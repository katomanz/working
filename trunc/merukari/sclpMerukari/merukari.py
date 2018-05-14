# -*- coding: utf-8 -*-
import sys
import os
import glob
import pandas
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

def getSeriesFromItemsbox(url):
    # Load URL to browser
    browser2.get(url)

    # Get title
    title = getText_find_element_by_css_selector(browser2, "h2.item-name")

    # Get price
    price = getText_find_element_by_css_selector(browser2, "span.item-price")

    # Get URL
    pageUrl = stringBaseUrl + url[url.rfind('/')+1:]
    pageUrl = pageUrl.replace(".html","")

    # Get Owner
    trs = browser2.find_element_by_class_name("item-detail-table").find_elements_by_css_selector("tr")
    for tr in trs:
        strTh = getText_find_element_by_css_selector(tr,"th")
        if (strTh == stringOwner_Utf8):
            owner = getText_find_element_by_css_selector(tr,"td a")

    isSold = 0
    if len(getText_find_element_by_css_selector(browser2, ".item-sold-out-badge")) > 0:
        isSold = 1

    # Get sub category and sub-sub category
    sub_category     = getText_find_element_by_css_selector(browser2, ".item-detail-table-sub-category")
    sub_sub_category = getText_find_element_by_css_selector(browser2, ".item-detail-table-sub-sub-category")

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

# Get Html file only
def getHtmlFromItemsbox(url):
    browser2.get(url)
    return BeautifulSoup(browser2.page_source, 'html.parser')

# Save Html file to the specified path
def saveHtmlFile(soup, path, fileName):
    # Create  characters
    with open(path + fileName, mode='w', encoding='utf-8') as fw:
        fw.write(soup.prettify())

# Crowling pages, paramter is URL
def crowling(num_page, url):
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

                ## Crawling only
                soup = getHtmlFromItemsbox(url)
                itemID = url.replace(stringBaseUrl, '').strip('/')
                saveHtmlFile(soup, stringPathToTmpHtml + dataSetName + "/", itemID + ".html")

                ## Scraping without tmp html
                #se = getSeriesFromItemsbox(url)
                #df = df.append(se, ignore_index=True)

            # Increment page number
            page+=1

            print("Next url:{}".format(btn))
            browser1.get(btn)
            print("Moving to next page......")

        # There isn't next page
        else:
            print("no pager exist anymore")
            break

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

# Initialize browser
#browser1 = webdriver.PhantomJS()
#browser2 = webdriver.PhantomJS()
browser1 = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
browser2 = webdriver.Chrome(executable_path='/usr/bin/chromedriver')

# Read csv file
df = pandas.read_csv(stringCsvFileName, index_col=0)

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
 "&" + stringKeyword +              "=" + "{}".format(query))  # Keyword

# Continue to crowling until specified page
crowling(num_page=20, url=webUrl)

# Scraping
tmpHtmlList = sorted(
    glob.glob(stringPathToTmpHtml + dataSetName + "/*"), key=os.path.getmtime)

for tmpHtml in tmpHtmlList:
    tmp = "file:///" + os.getcwd() + "/" + tmpHtml
    se = getSeriesFromItemsbox(tmp)
    df = df.append(se, ignore_index=True)

df.to_csv(stringPathToDatum + dataSetName + ".csv", encoding="utf-8", sep='\t')

# Close browser
browser1.quit()
browser2.quit()

# Return csv file name
sys.exit(dataSetName + ".csv")
