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

############################
###### Setting        ######
############################
pd.set_option("display.max_colwidth", 200)

############################
###### Process        ######
############################
# Get parameter from command line
args = sys.argv
argc = len(args)
# Check parameter
if (argc != 2):
    print ('Usage: # python %s csv_filename_to_analize' % args[0])
    quit()

# Check and set directory name
query = args[1]

# Get data set name
dataSetName = query.replace(".csv", "")

# Create tmp directory date + query
if os.path.isdir(stringPathToAnalizeTmpHtml + dataSetName) != True:
    os.mkdir(stringPathToAnalizeTmpHtml + dataSetName)

csv_data = pd.read_table(stringPathToDatum + query)
csv_data.fillna('No Brand', inplace=True)

# Added new columns for link columns
csv_data['stringForLink1'] = stringForLink1
csv_data['stringForLink2'] = stringForLink2
csv_data['stringForLink3'] = stringForLink3
csv_data['tileWithLink'] = csv_data['stringForLink1'] + csv_data['url'] + csv_data['stringForLink2'] + csv_data['title'] + csv_data['stringForLink3']

# Added imgUrl column
for  index, row in csv_data.iterrows():
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
    del htmlData['url']
    del htmlData['title']
    del htmlData['stringForLink1']
    del htmlData['stringForLink2']
    del htmlData['stringForLink3']
    del htmlData['sub_category']
    del htmlData['sub_sub_category']
    del htmlData['brand']
    del htmlData['sold']
    filename = "/rank" + '{0:02d}'.format(rank) + ".html"
    filepath = stringPathToAnalizeTmpHtml + dataSetName + filename
    htmlData.to_html(filepath)

    # Get brand name + sub-sub-category string
    brandCategory = index_name + ": " + str(item)
    priceAve = "{0:.2f}".format(htmlData['price'].mean())
    brandCategoryPrice = brandCategory + " Ave: " + str(priceAve) + "yen"
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

sys.exit(htmlFileName)
