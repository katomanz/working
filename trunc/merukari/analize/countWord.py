# -*- coding: utf-8 -*-
import MeCab
import sys
import os
import string
import codecs
from collections import OrderedDict
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../lib')
from cleaning import *
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import os
import urllib.request
from cleaning import *

class CountWords:
    path = "stop_words.txt"

    def __init__(self):
        if os.path.exists(self.path) == False:
            print("stop_words.txt isn't here... Download..")
            download_stopwords(path)
        self.stop_words = self.create_stopwords(self.path)
        pass
    
    def __del__(self):
        print("countWord() is disposed")
        pass

    def get_wakati_keywords(self, infile):
        t = MeCab.Tagger ('-d /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd')
        with codecs.open(infile, 'r', 'utf-8',) as fin:
            text = fin.read()
            otext = clean_text(text)
            res = t.parse(otext)
            info_of_words = res.split('\n')

            words = []
            dumps = []
            for info in info_of_words:
                if '\t' in info:
                    kind = info.split('\t')[1].split(',')[0]
                    category = info.split('\t')[1].split(',')[1]
                    if (kind == '名詞' and (category == '固有名詞' or category == '一般')):
                        words.append(info.split('\t')[0])
                    else:
                        dumps.append(info.split('\t')[0])
            with codecs.open("dumps.log", 'w', 'utf-8') as fout:
                for ele in dumps:
                    fout.write(ele+'\n')
        
        return words

    def download_stopwords(self, path):
        url = 'http://svn.sourceforge.jp/svnroot/slothlib/CSharp/Version1/SlothLib/NLP/Filter/StopWord/word/Japanese.txt'
        if os.path.exists(path):
            print('File already exists.')
        else:
            print('Downloading...')
            # Download the file from `url` and save it locally under `file_name`:
            urllib.request.urlretrieve(url, path)

    def create_stopwords(self, file_path):
        stop_words = []
        for w in open(self.path, "r"):
            w = w.replace('\n','')
            if len(w) > 0:
                stop_words.append(w)
        return stop_words

args = sys.argv
argc = len(args)

# Check parameter
if (argc != 2):
    print ('Usage: # python %s file_name' % args[0])
    quit()

filename = args[1]

c = CountWords()

# Run CountVectorizer
txt_vec = CountVectorizer(stop_words=c.stop_words)
words = c.get_wakati_keywords(filename)
txt_vec.fit_transform([' '.join(words)])

# Count number of words
print("Total num of words: " + str(len(txt_vec.get_feature_names())))

# extract parameter
word = txt_vec.transform([' '.join(words)])

# Get parater vector (Frequency)
vector = word.toarray()

# Output word and its frequency 
list = []
for word,count in zip(txt_vec.get_feature_names()[:], vector[0, :]):
    list.append([word, count])

df = pd.DataFrame(list)
df.columns = ['word', 'count']
df['count'] = df['count'].astype(int)
df = df.sort_values(by=['count'], ascending=False)
df.to_csv(filename + ".csv", index=False)
print("Calculation completed... Output: " + filename + ".csv")