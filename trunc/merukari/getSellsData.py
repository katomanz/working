from sclpMerukari.merukari import Merukari
from dataUpload.dataUpload import DataUpload
import sys
import os

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
d.dataUploadFileName("古着_2019-05-05.csv")

# Analyse data file
#print("Let's start analysing!")
#d = DataUpload()
#htmlfilename = d.dataUploadFileName(filename)

# Upload csv
#d = DataUpload()
#d.dataUploadFileName(htmlfilename)

# Send notification

