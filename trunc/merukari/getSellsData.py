from sclpMerukari.merukari import Merukari
from dataUpload.dataUpload import DataUpload
from analize.analize import Analyze
from notification import Notification
import sys
import os
import time

# For calculate process time
start_time = time.time()

args = sys.argv
argc = len(args)
# Check parameter
if (argc != 2):
    print ('Usage: # python %s csv_filename_to_analize' % args[0])
    quit()

# Check and set directory name
query = args[1]

# Scraping
print("Let's start searching!")
m = Merukari()
filename = m.getMerukariCSV(query, argc, args)

# Upload csv
d = DataUpload()
d.dataUploadFileName(filename)
del d

# Analyse data file
print("Let's start analysing!")
a = Analyze()
htmlFilename = a.analyzeCsvData("古着_2019-05-05.csv")

# Upload csv
d = DataUpload()
d.dataUploadFileName(htmlFilename)
del d

# Send notification
n = Notification()
n.sendNotification(query, filename, htmlFilename)

# Output process time 
elapsed_time = time.time() - start_time
print("Elapsed time is {0}".format(elapsed_time) + "[sec]")
