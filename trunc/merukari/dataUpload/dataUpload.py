# -*- coding: utf-8 -*-
import sys
import os
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

stringPathDatum="../datum/"
folder_id=os.environ["GOOGLEDRV_FLDR_ID"]

# Get parameter from command line
args = sys.argv
argc = len(args)
# Check parameter
if (argc != 2):
    print ('Usage: # python %s filename_to_updaload' % args[0])
    quit()

# Get date
today = datetime.date.today()

# Get file name to upload
query = args[1]
filename = "{0}_{1}.csv".format(query, today)

gauth = GoogleAuth()
gauth.CommandLineAuth()

drive = GoogleDrive(gauth)

# Make sure to add the path to the file to upload below.
f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder_id}], "title": filename})
f.SetContentFile(stringPathDatum + filename)
f.Upload()

# Show upload result
print(f['title'], f['id'])
