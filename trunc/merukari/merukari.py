import sys
import os
from selenium import webdriver
import pandas
import time

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

# Initialize browser
browser = webdriver.Chrome(executable_path='/usr/bin/chromedriver')

# Read csv file
df = pandas.read_csv(stringCsvFileName, index_col=0)
query = args[1]

# Get URL, Setting of serch setting
browser.get(stringMerikariUrl + stringSerch +
 "?" + stringSortOrder +            "=" + stringCreatedDesc +  # Sort
 "&" + stringStatusTradingSoldOut + "=" + "1" +                # Status "sold out"
#"&" + stringStatusOnSale +         "=" + "1" +                # Status "On sale"
 "&" + stringPriceMin +             "=" + stingPriceMinValue + # Minimum price
 "&" + stringKeyword +              "=" + "{}".format(query))  # Keyword

page = 1

#Continue until specified page
while page!=2:
    if len(browser.find_elements_by_css_selector("li.pager-next .pager-cell:nth-child(1) a")) > 0:
        print("######################page: {} ########################".format(page))
        print("Starting to get posts...")

        #5-1-2
        posts = browser.find_elements_by_css_selector(".items-box")

        #5-1-3
        for post in posts:
            title = post.find_element_by_css_selector("h3.items-box-name").text

            #5-1-3-1
            price = post.find_element_by_css_selector(".items-box-price").text
            price = price.replace(unichr(165), '')


            #5-1-3-2
            sold = 0
            if len(post.find_elements_by_css_selector(".item-sold-out-badge")) > 0:
                sold = 1

            url = post.find_element_by_css_selector("a").get_attribute("href")
            se = pandas.Series([title,price,sold,url],['title','price','sold','url'])
            df = df.append(se, ignore_index=True)

        #5-1-4
        page+=1

        btn = browser.find_element_by_css_selector("li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")
        print("next url:{}".format(btn))
        browser.get(btn)
        print("Moving to next page......")

    #5-2
    else:
        print("no pager exist anymore")
        break

#df.replace('0xa5','')
df.to_string()
print(df)
browser.quit()
