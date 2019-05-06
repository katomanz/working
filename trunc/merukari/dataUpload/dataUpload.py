# -*- coding: utf-8 -*-
import sys
import os
import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class DataUpload:
    stringPathDatum="../datum/"
    folder_id=os.environ["GOOGLEDRV_FLDR_ID"]
    def __init__(self):
        print("Change directory to dataUpload.")
        os.chdir("./dataUpload")
        pass

    def __del__(self):
        print("Change back directory.")
        os.chdir("..")

    def dataUploadFileName(self, filename):
        gauth = GoogleAuth()
        # Try to load saved client credentials
        gauth.LoadCredentialsFile("mycreds.txt")
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile("mycreds.txt")

        drive = GoogleDrive(gauth)

        # Make sure to add the path to the file to upload below.
        f = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": self.folder_id}], "title": filename})
        f.SetContentFile(self.stringPathDatum + filename)
        f.Upload()

        # Show upload result
        print(f['title'], f['id'])
