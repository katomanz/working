# -*- coding: utf-8 -*-
import sys
import os
import glob
import pandas
import time
from datetime import datetime
import random
import string
from decimal import (Decimal, ROUND_DOWN)
import pytz

# format of csv file
stringCsvFileName="default.csv"

# Get parameter from command line
args = sys.argv
argc = len(args)
# Check parameter
if (argc <  3):
    print ('Usage: # python %s can_log_file gps_log_file' % args[0])
    quit()

canFileName = args[1]
gpsFileName = args[2]

id = canFileName.replace(".log", "").replace("can_", "")

# File open
can_csv = pandas.read_csv(canFileName, sep=" ", names=('time', 'can0', 'signaldata'))

with open(gpsFileName, "rb") as gps_fp:
    lines = gps_fp.readlines()
for line in lines:
    line = str(line.decode('utf-8', 'ignore'))

gps_lines_strip = [str(line.strip() for line in lines)]

# Read default csv for result file
df = pandas.read_csv(stringCsvFileName, index_col=0)

# preprocess
for  index, row in can_csv.iterrows():
    can_csv.at[index,'time'] = can_csv.at[index,'time'].strip("(").strip(")")

del can_csv['can0']
p_time = ""

# Remove row until kirino ii tokoro
for index, row in can_csv.iterrows():
    time = can_csv.at[index,'time']
    time = time.split('.')[0][:-1]
    if p_time != time and index > 2:
        break
    p_time = time
    can_csv = can_csv.drop(index)

# ato ha 60 gyou goto ni syori
num = 1
for index, row in can_csv.iterrows():
    if (num == 10):
        soc = int(can_csv.at[index, 'signaldata'][-4:-2], 16)
    if (num == 11):
        soh = int(can_csv.at[index, 'signaldata'][11:13], 16)
    if (num == 32):
        # syousuu dai ichii made syutsuryoku
        batteryTempHigh = Decimal(int(can_csv.at[index, 'signaldata'][15:19], 16) * 0.1).quantize(Decimal('0.1'), rounding=ROUND_DOWN)
        batteryTemplow = Decimal(int(can_csv.at[index, 'signaldata'][19:23], 16) * 0.1).quantize(Decimal('0.1'), rounding=ROUND_DOWN)
    if (num == 44):
        speed = int(can_csv.at[index, 'signaldata'][13:15], 16)
    if (num == 58):
        odd_pre = can_csv.at[index, 'signaldata'][-4:]
        odd_post = can_csv.at[index+1, 'signaldata'][11:13]
        oddmeter = int(odd_pre + odd_post, 16)
    if (num == 60):
        unitime = can_csv.at[index, 'time']
        timestamp = str(datetime.fromtimestamp(float(unitime)))
        timestamp_utc = str(datetime.utcfromtimestamp(float(unitime)))
        gprmcStr = "$GPRMC,"
        hhmmss = timestamp_utc[11:19].replace(':', '')
        gprm = ""
        # hairetsu no naka kara tokuteino mojiretsu no haitta gyou wo sagasu
        for line in lines:
            if gprmcStr+hhmmss in line.decode('utf-8', 'ignore'):
                gprm = line.decode('utf-8', 'ignore').replace('\n', '')
    
        latitude = ""
        longitude = ""
        if len(gprm) != 0:
            latitude = gprm.split(',')[3]
            longitude = gprm.split(',')[5]

        vehicleRange = ""
        se = pandas.Series([timestamp,oddmeter,soc,soh,latitude,longitude,batteryTempHigh,batteryTemplow,vehicleRange, speed],
                ['timestamp','odometer','soc','soh','latitude','longitude','temperatureHigh', 'temperatureLow', 'vehiclerange', 'speed'])
        se.str.encode(encoding="utf-8")
        df = df.append(se, ignore_index=True)
        num = 0
    num = num + 1

df.to_csv("res_"+ id + ".csv", encoding="utf-8", sep=',')
