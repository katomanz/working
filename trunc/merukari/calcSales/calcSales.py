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
from bs4 import BeautifulSoup

stringTitleSalesHistory = u"過去の売上履歴"
stringForItemUtf8 = u"商品"
stringForSalesFeeUtf8 = u"販売手数料"
stringForSalesProfitUtf8 = u"販売利益"
stringForSoldTimeUtf8 = u"購入日時"
stringForItemIDUtf8 = u"商品ID"
# format of csv file
stringCsvFileName="./default.csv"

############################
###### Function       ######
############################
# Get find element by css selector
def getText_find_element_by_css_selector(browser, cssSel):
    try:
        ret = browser.find_element_by_css_selector(cssSel).text
    except:
        print("Could not find " + cssSel)
        ret = "NA"
    finally:
        return ret

def getTransactionDataFromItemsLink(url):
    # Load URL to browser
    browser1.get(url)

    rows = browser1.find_elements_by_class_name("transact-info-table-row")
    for row in rows:
        columns = row.find_elements_by_class_name("transact-info-table-cell")
        if stringForItemUtf8 == columns[0].text:
            tmp = columns[1].text.split("\n")
            title = tmp[0]
            soldPrice = tmp[1].replace("¥ ", "").replace(",", "")
        elif stringForSalesFeeUtf8 == columns[0].text:
            salesFee = columns[1].text.replace("¥ ", "").replace(",", "")
        elif stringForSalesProfitUtf8 == columns[0].text:
            tmp1 = columns[1].text.split("\n")
            salesProfit = tmp1[0].replace("¥ ", "").replace(",", "")
        elif stringForSoldTimeUtf8 == columns[0].text:
            soldTime = columns[1].text
        elif stringForItemIDUtf8 == columns[0].text:
            itemId = columns[1].text

    se = pandas.Series([itemId, title, soldPrice, salesFee, salesProfit, soldTime],
                    ['itemId', 'title', 'soldPrice', 'salesFee', 'salesProfit', 'soldTime'])
    se.str.encode(encoding="utf-8")
    return se

browser1 = webdriver.Chrome(executable_path='/usr/bin/chromedriver')
#browser1 = webdriver.Chrome(executable_path='C:\DRIVER\webdriver\chromedriver.exe')

#browser1.get("file:///" + os.getcwd() + "/" + "salesdata.html")
browser1.get("https://www.mercari.com/jp/mypage/sales/histories/")

email = browser1.find_element_by_name('email')
email.send_keys(os.environ["EMAIL"])
password = browser1.find_element_by_name('password')
password.send_keys(os.environ["PASSWORD"])

# Wait Log in process
while True:
    time.sleep(10)
    print(browser1.current_url)
    if u"売上履歴" in browser1.page_source:
        print('Log-in dekitane! Watshi Ureshii!!')
        break

df = pandas.DataFrame(columns=['itemId', 'title', 'soldPrice', 'salesFee', 'salesProfit', 'soldTime'])
posts = browser1.find_elements_by_css_selector("section ul li a")
urllist = []
for post in posts:
    try:
        salesDataCategory = post.find_element_by_class_name("l-left").text
        url = post.get_attribute("href")
        if "order_status" in url and stringForSalesProfitUtf8 in salesDataCategory:
            urllist.append(url)
    except NoSuchElementException as e:
        print(e)
    except UnboundLocalError as e:
        print(urllist)

print("Totally " + str(len(urllist)) + " records were found..")
for url in urllist:
    try:
        #se = getTransactionDataFromItemsLink("file:///" + os.getcwd() + "/" + "eachdata.html")
        se = getTransactionDataFromItemsLink(url)
        df = df.append(se, ignore_index=True)
    except NoSuchElementException as e:
        print(e)
    except UnboundLocalError as e:
        print(df)

df.to_csv("salesdata.csv", encoding="utf-8", sep='\t', index=False)

browser1.quit()