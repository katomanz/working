# -*- coding: utf-8 -*-
import sys
import os
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

# format of csv file
stringCsvFileName="./sclpMerukari/default.csv"

# string for brand utf-8
stringBrand_Utf8=u"ブランド"

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

def getSeriesFromItemsbox(post):
    # Get price
    title = getText_find_element_by_css_selector(post, "h3.items-box-name")
    price = getText_find_element_by_css_selector(post, ".items-box-price")
    price = price.replace(chr(165), '') # Remove yen mark

    isSold = 0
    if len(post.find_elements_by_css_selector(".item-sold-out-badge")) > 0:
        isSold = 1

    url = post.find_element_by_css_selector("a").get_attribute("href")

    browser2.get(url)
    sub_category     = getText_find_element_by_css_selector(browser2, ".item-detail-table-sub-category")
    sub_sub_category = getText_find_element_by_css_selector(browser2, ".item-detail-table-sub-sub-category")

    # Get brand name
    trs = browser2.find_element_by_class_name("item-box-container").find_elements_by_css_selector("tr")
    for tr in trs:
        strTh = getText_find_element_by_css_selector(tr,"th")
        if (strTh == stringBrand_Utf8):
            brand = getText_find_element_by_css_selector(tr,"td")

    se = pandas.Series([title,price,isSold,url,sub_category,sub_sub_category,brand],
                       ['title','price','sold','url','sub_category','sub_sub_category','brand'])
    se.str.encode(encoding="utf-8")
    return se

# Get Html file only
def getHtmlFromItemsbox(post):
    # Get Url 
    url = post.find_element_by_css_selector("a").get_attribute("href")
    browser2.get(url)
    return BeautifulSoup(browser2.page_source, 'html.parser')

# Save Html file to the specified path 
def saveHtmlFile(soup, path):
    # Create random filename 10 characters
    randomFileName = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    with open(path + randomFileName + '.html', mode = 'w', encoding = 'utf-8') as fw:
        fw.write(soup.prettify())

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
browser1 = webdriver.PhantomJS()
browser2 = webdriver.PhantomJS()

# Read csv file
df = pandas.read_csv(stringCsvFileName, index_col=0)

query = args[1]

dataSetName = "{0}_{1}".format(query, today)

# Create tmp directory date + query
if os.path.isdir(stringPathToTmpHtml + dataSetName) != True:
    os.mkdir(stringPathToTmpHtml + dataSetName)

# Get URL, Setting of serch setting
browser1.get(stringMerikariUrl + stringSerch +
 "?" + stringSortOrder +            "=" + stringCreatedDesc +  # Sort
 "&" + stringStatusTradingSoldOut + "=" + "1" +                # Status "sold out"
#"&" + stringStatusOnSale +         "=" + "1" +                # Status "On sale"
 "&" + stringPriceMin +             "=" + stingPriceMinValue + # Minimum price
 "&" + stringKeyword +              "=" + "{}".format(query))  # Keyword

page = 1

#Continue until specified page
while page!=20:
    if len(browser1.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) > 0:
        print("######################page: {} ########################".format(page))
        print("Starting to get posts...")

        posts = browser1.find_elements_by_css_selector(".items-box")
        # Get next page url
        btn = browser1.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")

        for post in posts:
            ## Scraping without tmp html
            # se = getSeriesFromItemsbox(post)
            # df = df.append(se, ignore_index=True)

            ## Scraping with tmp html
            soup = getHtmlFromItemsbox(post)
            saveHtmlFile(soup, stringPathToTmpHtml + dataSetName + "/")

        # Increment page number
        page+=1

        print("Next url:{}".format(btn))
        browser1.get(btn)
        print("Moving to next page......")

    # There isn't next page
    else:
        print("no pager exist anymore")
        break

df.to_csv(stringPathToDatum + dataSetName + ".csv", encoding="utf-8", sep='\t')

# Close browser
browser1.quit()
browser2.quit()
