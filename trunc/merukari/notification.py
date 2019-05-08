# -*- coding: utf-8 -*-
import requests
import sys
import os

class Notification:
    def __init__(self):
        pass
    def __del__(self):
        pass
    
    def sendNotification(self, query, csvFilename, htmlFilename):
        line_notify_api = 'https://notify-api.line.me/api/notify'
        message = query + ': search was done.\n' + csvFilename + '\n' + htmlFilename + '\n'

        payload = {'message': message}
        headers = {'Authorization': 'Bearer ' + os.environ["LINE_NOTIFY_TOKEN"]}
        line_notify = requests.post(line_notify_api, data=payload, headers=headers)
    