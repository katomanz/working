# -*- coding: utf-8 -*-
import sys
import os
import datetime
import numpy as np
import pandas as pd
import random
import glob
import time
import random
import string
from xml.sax.saxutils import unescape
#import matplotlib.pyplot as plt
#pd.options.display.mpl_style = 'default'

############################
###### Setting        ######
############################
pd.set_option("display.max_colwidth", 200)

############################
###### Strings        ######
############################
# string for link
stringForLink1="<a href=\""
stringForLink2="\" target=\"_blank\">"
stringForLink3="</a>"

# Path to tmpHtml
stringPathToTmpHtml="./analize/tmpHtml/"

# Path to Datum
stringPathToDatum="./datum/"

# String for details
stringForDetailsStart="<details>"

# String for details
stringForDetailsEnd="</details>"

# String for Summary
stringForSummary="<summary>REPLACE</summary>"

# String for template html name
stringForTemplateHtml="./analize/template.html"

############################
###### Function       ######
############################
def random_string(length, seq='0123456789abcdefghijklmnopqrstuvwxyz'):
    sr = random.SystemRandom()
    return ''.join([sr.choice(seq) for i in range(length)])

# Save Html file to the specified path
def saveHtmlFile(soup, path, fileName):
    # Create  characters
    with open(path + fileName, mode='w', encoding='utf-8') as fw:
        fw.write(soup.prettify())

def replaceEscapeHtmlString(filename):
    # Read in the file
    with open(filename, 'r') as file :
        filedata = file.read()
        
    # Replace the target string
    filedata = filedata.replace('&lt;', '<')
    filedata = filedata.replace('&gt;', '>')
    
    # Write the file out again
    with open(filename, 'w') as file:
        file.write(filedata)


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

# Check and set directory name
query = args[1]

# Get date
today = datetime.date.today()
dataSetName = "{0}_{1}".format(query, today)

# Create tmp directory date + query
if os.path.isdir(stringPathToTmpHtml + dataSetName) != True:
    os.mkdir(stringPathToTmpHtml + dataSetName)

csv_data = pd.read_table(stringPathToDatum + query)
csv_data.fillna('No Brand', inplace=True)

# Added new columns for link columns
csv_data['stringForLink1'] = stringForLink1
csv_data['stringForLink2'] = stringForLink2
csv_data['stringForLink3'] = stringForLink3
csv_data['tileWithLink'] = csv_data['stringForLink1'] + csv_data['url'] + csv_data['stringForLink2'] + csv_data['title'] + csv_data['stringForLink3']

csv_data['brand-sub_sub_category'] = csv_data['brand'] + ' + ' + csv_data['sub_sub_category']

# Get top 20 brand-sub_sub_bategory
vc = csv_data['brand-sub_sub_category'].value_counts(dropna=False)
vc.columns = ['brand-sub_sub_category', 'count']

top20BSSC = vc.head(n=20)
rank = 1
for index_name, item in top20BSSC.iteritems():
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
    filepath = stringPathToTmpHtml + dataSetName + filename
    htmlData.to_html(filepath)
    brandCategory = index_name + ": " + str(item)
    brandCategoryElement = stringForSummary.replace('REPLACE', brandCategory)

    with open(filepath,'r') as htmlFile:
        l = htmlFile.readlines()
   
    l.insert(0, brandCategoryElement)
    with open(filepath, mode='w') as f:
        f.writelines(l)
    rank = rank + 1

tmpHtmlList = sorted(
    glob.glob(stringPathToTmpHtml + dataSetName + "/*"), key=os.path.getmtime)

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
