# -*- coding: utf-8 -*-
import requests
import sys
import os

# Get parameter from command line
args = sys.argv
argc = len(args)
# Check parameter
if (argc != 4):
    print('Usage: # python %s keyword_to_notify' % args[0])
    quit()

line_notify_api = 'https://notify-api.line.me/api/notify'
message = query = args[1] + ': search was done.\n' + args[2] + '\n' + args[3] + '\n'

payload = {'message': message}
headers = {'Authorization': 'Bearer ' + os.environ["LINE_NOTIFY_TOKEN"]}
line_notify = requests.post(line_notify_api, data=payload, headers=headers)
