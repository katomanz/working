# -*- coding: utf-8 -*-
import sys
import os
import datetime
import numpy as np
import pandas as pd
import glob
import time
import random
import string
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../lib')
from const import *
from utility import *

class Analyze:
    def __init__(self):
        # Setting for pandas
        pd.set_option("display.max_colwidth", 200)
        pass

    def __del__(self):
        pass

    def analyzeCsvData(self, csvFileName):

        dataSetName = csvFileName.rstrip(".csv")

        # Create tmp directory date + dataSetName
        if os.path.isdir(stringPathToAnalizeTmpHtml + dataSetName) != True:
            os.mkdir(stringPathToAnalizeTmpHtml + dataSetName)

        csv_data = pd.read_csv(stringPathToDatum + csvFileName, sep='\t')
        csv_data.fillna('No Brand', inplace=True)

        # Added new columns for link columns
        csv_data['stringForLink1'] = stringForLink1
        csv_data['stringForLink2'] = stringForLink2
        csv_data['stringForLink3'] = stringForLink3
        csv_data['tileWithLink'] = csv_data['stringForLink1'] + csv_data['pageUrl'] + csv_data['stringForLink2'] + csv_data['title'] + csv_data['stringForLink3']

        # Added imgUrl column
        for index, row in csv_data.iterrows():
            csv_data.at[index,'imgUrl'] = stringForImgLink1 + csv_data.at[index,'imgUrl'] + stringForImgLink2

        csv_data['brand-sub_sub_category'] = csv_data['brand'] + ' + ' + csv_data['sub_sub_category']

        # Get top 20 brand-sub_sub_bategory
        vc = csv_data['brand-sub_sub_category'].value_counts(dropna=False)
        vc.columns = ['brand-sub_sub_category', 'count']

        topBSSC = vc.head(n=30)
        rank = 1
        for index_name, item in topBSSC.iteritems():
            htmlData = csv_data[csv_data['brand-sub_sub_category'] == index_name]
            # Delete unnecessary columns
            del htmlData['Unnamed: 0']
            del htmlData['pageUrl']
            del htmlData['title']
            del htmlData['stringForLink1']
            del htmlData['stringForLink2']
            del htmlData['stringForLink3']
            del htmlData['sub_category']
            del htmlData['sub_sub_category']
            del htmlData['brand']
            del htmlData['isSold']
            del htmlData['description']
            del htmlData['ownerId']
            filename = "/rank" + '{0:02d}'.format(rank) + ".html"
            filepath = stringPathToAnalizeTmpHtml + dataSetName + filename
            htmlData.to_html(filepath)

            # Get brand name + sub-sub-category string
            brandCategory = index_name + ": " + str(item)
            
            priceAve = "{0:.2f}".format(float(htmlData['price'].mean()))
            
            brandCategoryPrice = brandCategory + " Ave: " + str(1000) + "yen"
            brandCategoryElement = stringForSummary.replace('REPLACE', brandCategoryPrice)
            
            with open(filepath,'r') as htmlFile:
                l = htmlFile.readlines()
        
            l.insert(0, brandCategoryElement)
            with open(filepath, mode='w') as f:
                f.writelines(l)
            rank = rank + 1

        tmpHtmlList = sorted(
            glob.glob(stringPathToAnalizeTmpHtml + dataSetName + "/*"), key=os.path.getmtime)

        for tmpHtml in tmpHtmlList:
            tmp = os.getcwd() + "/" + tmpHtml
            replaceEscapeHtmlString(tmp)

        # Read Template html
        temlateHtml = open(stringForTemplateHtml, "r")
        tmplate = temlateHtml.read()

        htmlFileName = dataSetName + ".html"
        with open(stringPathToDatum + htmlFileName, 'w') as f:
            f.write(tmplate + '\n')
            for file in tmpHtmlList:
                with open(file) as infile:
                    f.write(stringForDetailsStart+'\n')
                    f.write(infile.read()+'\n')
                    f.write(stringForDetailsEnd+'\n')

        return htmlFileName
