from sclpMerukari.merukari import Merukari
from dataUpload.dataUpload import DataUpload
from analize.analize import Analyze
from notification import Notification
import sys
import os
import time
import argparse

# For calculate process time
start_time = time.time()

# Initialize parameter
parser = argparse.ArgumentParser(description='Extract data from mercari')
parser.add_argument('query', help='Input keyword of Search')
parser.add_argument('-s', '--scrape', action='store_true')
parser.add_argument('-g', '--getdtl', action='store_true')

args = parser.parse_args()

# Scraping
print("Let's start searching!")
m = Merukari()
filename = m.getMerukariCSV(args.query, args)

if (args.scrape == False and args.getdtl == False):
    # Upload csv
    d = DataUpload()
    d.dataUploadFileName(filename)
    del d

    # Analyse data file
    print("Let's start analysing!")
    a = Analyze()
    htmlFilename = a.analyzeCsvData(filename)

    # Upload csv
    d = DataUpload()
    d.dataUploadFileName(htmlFilename)
    del d

    # Send notification
    n = Notification()
    n.sendNotification(args.query, filename, htmlFilename)

# Output process time 
elapsed_time = time.time() - start_time
print("Elapsed time is {0}".format(elapsed_time) + "[sec]")
