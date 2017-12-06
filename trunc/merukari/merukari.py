# -*- coding: utf-8 -*-
import sys
import os
from selenium import webdriver
import pandas
import time
import datetime
from selenium.common.exceptions import NoSuchElementException

############################
###### Strings        ######
############################
# URL sting
stringMerikariUrl="https://www.mercari.com/jp/"
stringSerch="search/"

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
stringCsvFileName="default.csv"

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
    title = getText_find_element_by_css_selector(post, "h3.items-box-name")
    price = getText_find_element_by_css_selector(post, ".items-box-price")
    price = price.replace(unichr(165), '')


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

    se = pandas.Series([title,price,isSold,url,sub_category,sub_sub_category,brand],['title','price','sold','url','sub_category','sub_sub_category','brand'])
    se.str.encode(encoding="utf-8")
    return se

############################
###### Process        ######
############################

# Get parameter from command line
args = sys.argv
argc = len(args)
# Check parameter
if (argc != 2):
    print 'Usage: # python %s keyword_to_serch' % args[0]
    quit()

# Get date
today = datetime.date.today()

# Initialize browser
browser1 = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
browser2 = webdriver.Chrome(executable_path='/usr/bin/chromedriver')

# Read csv file
df = pandas.read_csv(stringCsvFileName, index_col=0)

query = args[1]

# Get URL, Setting of serch setting
browser1.get(stringMerikariUrl + stringSerch +
 "?" + stringSortOrder +            "=" + stringCreatedDesc +  # Sort
 "&" + stringStatusTradingSoldOut + "=" + "1" +                # Status "sold out"
#"&" + stringStatusOnSale +         "=" + "1" +                # Status "On sale"
 "&" + stringPriceMin +             "=" + stingPriceMinValue + # Minimum price
 "&" + stringKeyword +              "=" + "{}".format(query))  # Keyword

page = 1

#Continue until specified page
while page!=2:
    if len(browser1.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) > 0:
        print("######################page: {} ########################".format(page))
        print("Starting to get posts...")

        posts = browser1.find_elements_by_css_selector(".items-box")
        # Get next page url
        btn = browser1.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")

        for post in posts:
            se = getSeriesFromItemsbox(post)
            df = df.append(se, ignore_index=True)

        # Increment page number
        page+=1

        print("next url:{}".format(btn))
        browser1.get(btn)
        print("Moving to next page......")

    #5-2
    else:
        print("no pager exist anymore")
        break

df.to_csv("{0}_{1}.csv".format(query, today), encoding="utf-8")

# Close browser
browser1.quit()
browser2.quit()
