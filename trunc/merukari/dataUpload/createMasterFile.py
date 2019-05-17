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

class createMasterFile:
    fileName = "MasterResult.csv"
    save_location = "./tmp/summary"
    data_location = "./tmp/"
    def __init__(self):
        pd.set_option('display.max_columns', 50)
        pass

    def __del__(self):
        pass

    def createMaster(self):
        tmpFileList = sorted(
            glob.glob(self.data_location + "*" + ".csv"), key=os.path.getmtime)

        list = []
        for tmpFile in tmpFileList:
            print(tmpFile)
            list.append(pd.read_csv(tmpFile, sep="\t"))

        df = pd.concat(list, sort=False)
        del df['Unnamed: 0']
        df.drop_duplicates(subset='url', inplace=True)
        df.to_csv(self.fileName, encoding='utf_8', sep="\t", index=False)

c = createMasterFile()
c.createMaster()