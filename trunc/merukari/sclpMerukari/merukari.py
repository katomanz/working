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
class Merukari:
    # Initialize browser
    dataSetName = ""

    def __init__(self):
        # Initialize browser
        options = Options()
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.add_argument('--headless')

        self.browser1 = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
        self.browser2 = webdriver.Chrome(chrome_options=options, executable_path='/usr/bin/chromedriver')
        #browser1 = webdriver.Chrome(chrome_options=options, executable_path='C:\DRIVER\webdriver\chromedriver.exe')
        #browser2 = webdriver.Chrome(chrome_options=options, executable_path='C:\DRIVER\webdriver\chromedriver.exe')

    def __del__(self):
        print("Merukari() is disposed")
        
    def getUrl(self, browser, url):
        try:
            browser.get(url)
        except RemoteDisconnected as e:
            print(e)
            pass

    def getSeriesFromItemsbox(self, url, price):
        # Load URL to browser
        self.getUrl(self.browser2, url)
        
        ##  Save Html files just in case
        itemID = url.replace(stringBaseUrl, '').split('/')
        soup = BeautifulSoup(self.browser2.page_source, 'html.parser')
        saveHtmlFile(soup, stringPathToTmpHtml + self.dataSetName + "/", itemID[0] + ".html")

        # Get title
        title = getText_find_element_by_css_selector(self.browser2, stringItemName)

        # Get URL
        pageUrl = url[:url.rfind('?')-1]

        # Get Owner
        trs = self.browser2.find_element_by_class_name(stringItemDetailTable).find_elements_by_css_selector("tr")
        for tr in trs:
            strTh = getText_find_element_by_css_selector(tr,"th")
            if (strTh == stringOwner_Utf8):
                owner = getText_find_element_by_css_selector(tr,"td a")

        isSold = 0
        if len(getText_find_element_by_css_selector(self.browser2, stringItemSoldOutBadge)) > 0:
            isSold = 1

        # Get sub category and sub-sub category
        sub_category     = getText_find_element_by_css_selector(self.browser2, stringItemDetailTableSubCategory)
        sub_sub_category = getText_find_element_by_css_selector(self.browser2, stringItemDetailTableSubSubCategory)

        # Get brand name
        trs = self.browser2.find_element_by_class_name("item-box-container").find_elements_by_css_selector("tr")
        for tr in trs:
            strTh = getText_find_element_by_css_selector(tr,"th")
            if (strTh == stringBrand_Utf8):
                brand = getText_find_element_by_css_selector(tr,"td")
        # Get imgUrl
        imgUrl = self.browser2.find_element_by_class_name("owl-item-inner").find_element_by_class_name("owl-lazy").get_attribute("data-src")
        post_timestamp = self.getItemPostTimeStamp(imgUrl)
        se = pandas.Series([post_timestamp, title,price,isSold,pageUrl,sub_category,sub_sub_category,brand,owner,imgUrl],
                        ['post_timestamp','title','price','sold','url','sub_category','sub_sub_category','brand','owner','imgUrl'])
        se.str.encode(encoding="utf-8")
        return se

    def getItemPostTimeStamp(self, url):
        r = requests.head(url)
        resJson = r.headers
        loadedDict = dict(resJson)
        timestamp = loadedDict["Last-Modified"]
        print(timestamp)
        return timestamp

    def getSeriesFromItemsboxFromLocalDirectory(self, url):
        # Load URL to browser
        self.getUrl(self.browser2, url)

        # Get title
        title = getText_find_element_by_css_selector(self.browser2, stringItemName)

        # Get URL
        pageUrl = stringBaseUrl + url[url.rfind('/')+1:]
        pageUrl = pageUrl.replace(".html","")

        # Get price
        price = getText_find_element_by_css_selector(self.browser2, stringItemPrice)
        price = price.replace("¥ ", "").replace(",", "")

        # Get Owner
        trs = self.browser2.find_element_by_class_name(stringItemDetailTable).find_elements_by_css_selector("tr")
        for tr in trs:
            strTh = getText_find_element_by_css_selector(tr,"th")
            if (strTh == stringOwner_Utf8):
                owner = getText_find_element_by_css_selector(tr,"td a")

        isSold = 0
        if len(getText_find_element_by_css_selector(self.browser2, stringItemSoldOutBadge)) > 0:
            isSold = 1

        # Get sub category and sub-sub category
        sub_category     = getText_find_element_by_css_selector(self.browser2, stringItemDetailTableSubCategory)
        sub_sub_category = getText_find_element_by_css_selector(self.browser2, stringItemDetailTableSubSubCategory)

        # Get brand name
        trs = self.browser2.find_element_by_class_name("item-box-container").find_elements_by_css_selector("tr")
        for tr in trs:
            strTh = getText_find_element_by_css_selector(tr,"th")
            if (strTh == stringBrand_Utf8):
                brand = getText_find_element_by_css_selector(tr,"td")

        se = pandas.Series([title,price,isSold,pageUrl,sub_category,sub_sub_category,brand,owner],
                        ['title','price','sold','url','sub_category','sub_sub_category','brand','owner'])
        se.str.encode(encoding="utf-8")
        return se

    def getDescriptionTextFromItemsbox(self, url):
        # Load URL to browser
        self.getUrl(self.browser2, url)

        # Get item desctiption
        des = getText_find_element_by_css_selector(self.browser2, "p.item-description-inner")
        return des

    # Scraping from local directory
    def scrapingFromLocalDirectory(self, directoryPath, df):
        tmpHtmlList = sorted(
            glob.glob(directoryPath), key=os.path.getmtime)

        for tmpHtml in tmpHtmlList:
            tmp = "file:///" + os.getcwd() + "/" + tmpHtml
            se = self.getSeriesFromItemsboxFromLocalDirectory(tmp)
            df = df.append(se, ignore_index=True)
        return df

    # scraping pages, paramter is URL
    def scrapelToGetDescription(self, num_page, url):
        self.getUrl(self.browser1, url)
        page = 1
        des = ""
        while page != num_page:
            if len(self.browser1.find_elements_by_css_selector(stringNextPage)) > 0:
                print("######################page: {} ########################".format(page))
                print("Starting to get posts...")

                posts = self.browser1.find_elements_by_css_selector(".items-box")
                # Get next page url
                btn = self.browser1.find_element_by_css_selector(
                    "li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")

                for post in posts:
                    url = post.find_element_by_css_selector("a").get_attribute("href")
                    des += self.getDescriptionTextFromItemsbox(url)

                # Increment page number
                page+=1

                print("Next url:{}".format(btn))
                self.getUrl(self.browser1, btn)
                print("Moving to next page......")

            # There isn't next page
            else:
                print("no pager exist anymore")
                break
        return des

    # Crowling pages, paramter is URL
    def crowling(self, num_page, url, df):
        self.getUrl(self.browser1, url)
        page = 1
        while page != num_page:
            if len(self.browser1.find_elements_by_css_selector(stringNextPage)) > 0:
                print("######################page: {} ########################".format(page))
                print("Starting to get posts...")

                posts = self.browser1.find_elements_by_css_selector(".items-box")
                # Get next page url
                btn = self.browser1.find_element_by_css_selector(
                    "li.pager-next .pager-cell:nth-child(1) a").get_attribute("href")

                for post in posts:
                    url = post.find_element_by_css_selector("a").get_attribute("href")

                    ## Scraping without tmp html
                    priceBox = getText_find_element_by_css_selector(post, ".items-box-price")
                    priceBox = priceBox.replace("¥ ", "").replace(",", "")

                    se = self.getSeriesFromItemsbox(url, priceBox)
                    df = df.append(se, ignore_index=True)

                # Increment page number
                page+=1

                print("Next url:{}".format(btn))
                self.getUrl(self.browser1, btn)
                print("Moving to next page......")

            # There isn't next page
            else:
                print("no pager exist anymore")
                break

        return df

    def getMerukariCSV(self, query, args):
        # Get date
        today = datetime.date.today()

        self.dataSetName = "{0}_{1}".format(query, today)

        # Get URL, Setting of serch setting
        webUrl = (stringMerikariUrl + stringSerch +
        "?" + stringSortOrder +            "=" + stringCreatedDesc +  # Sort
        "&" + stringCategoryRoot +         "=" + "2"               +  # root category 1=lady's 2=men's
        "&" + stringStatusTradingSoldOut + "=" + "1"               +  # Status "sold out"
        #"&" + stringStatusOnSale +         "=" + "1" +                # Status "On sale"
        "&" + stringPriceMin +             "=" + stingPriceMinValue + # Minimum price
        "&" + stringItemStatus +           "=" + "1"               +  # Status of Item
        "&" + stringKeyword +              "=" + "{}".format(query))  # Keyword

        # Create tmp directory date + query
        if os.path.isdir(stringPathToTmpHtml + self.dataSetName) != True:
            os.mkdir(stringPathToTmpHtml + self.dataSetName)

        if (args.scrape == True):
            # Scraping
            print("Option: --scrape")
            df = pandas.read_csv(stringCsvFileName, index_col=0)
            df = self.scrapingFromLocalDirectory(stringPathToTmpHtml + self.dataSetName + "/*", df=df)
            df.to_csv(stringPathToDatum + self.dataSetName + ".csv", encoding="utf-8", sep='\t')

        elif (args.getdtl == True):
            # Get item detail
            print("Option: --getdtl")
            text = self.scrapelToGetDescription(num_page=30, url=webUrl)
            with open(stringPathToDatum + self.dataSetName + ".txt", 'ab') as f:
                f.write(text.encode('utf-8', 'ignore'))
        else:
            # Continue to crowling until specified page
            print("Option: default")
            # Read csv file
            df = pandas.read_csv(stringCsvFileName, index_col=0)
            df = self.crowling(num_page=20, url=webUrl, df=df)
            df.to_csv(stringPathToDatum + self.dataSetName + ".csv", encoding="utf-8", sep='\t')

        # Close browser
        self.browser1.quit()
        self.browser2.quit()

        # Return csv file name
        return self.dataSetName + ".csv"
