# -*- coding: utf-8 -*-
import MeCab # 必要なモジュールを読み込み
import sys
import os
import string
import codecs
from collections import OrderedDict

from cleaning import *

# Parse infile 文章を解析して，結果をoutfileに出力
def morph_analysis(infile, outfile):
    t = MeCab.Tagger('mecabrc')
    with codecs.open(infile, 'r', 'utf-8',) as fin:
        with codecs.open(outfile, 'w', 'utf-8') as fout:
            text = fin.read()
            otext = clean_text(text)
            res = t.parse(otext)
            fout.write(res)

    return outfile

# 読み込んで解析器に渡し結果を受け取りそれを書き出すまで，すべてutf-8の文字列で行っている

# 解析結果のファイルを読み込む
def get_m_lines(file):
    with codecs.open(file, 'r', 'utf-8', 'ignore') as f: # 解析結果のファイルを開く
        m_lines = f.read().split('\n') # 読み込んで，改行で分割

        # m_linesの最後2つの要素はEOSと空白なのでカットしておく
        m_lines.pop(-1)
        m_lines.pop(-1)

    return m_lines

def noun_ha(mlines):
    hist = dict() # キーに名詞、値に頻度（数字）が入るのを想定
    morphs = []
    tr_hist = dict()

    for line in mlines:
        morphs.append(mecab_data(line)) #形態素を１つずつ辞書型に変換

    for i in range(len(morphs)):
        if morphs[i]['pos'] == '名詞':
            key = morphs[i]['surface'] #その名詞をキーとする
            hist[key] = hist.get(key,0) + 1 #もし、まだそのkeyが存在しなかったら(=初めて出現したら),デフォルト値を0と考えて1を足す。

    for noun in hist: #キーを取り出す
        #histは頻出回数がバリューだが、
        #tr_hist に　頻出回数をキーに変換したものを入れる。バリューを名詞のリストにする
        tr_hist[hist[noun]] = tr_hist.get(hist[noun],[])+[noun]

    #見やすく名詞ごとに出力、頻度高い順に
    for i in sorted(tr_hist.keys(), reverse = True):
        if i > 30: #頻出回数が30以上なら
            for m in range(len(tr_hist[i])):
                #同じ出現回数の名詞を分けて表示
                print( tr_hist[i][m], i)

# 文字列である解析結果を使いやすい形（辞書型）に
def mecab_data(line):
    mkeys = ['pos', 'pos1', 'pos2', 'pos3', 'inf', 'form', 'base', 'yomi', 'oto']
    morph = OrderedDict()
    # タブ以前が表記、それ以降が品詞データのため
    data = line.split('\t')
    morph['surface'] = data[0]

    features = data[1].split(',') # その他の情報はカンマ区切りなので，カンマで分割
    for i in range(len(features)) : # 分割されたそれぞれの情報を
        morph[mkeys[i]] = features[i] # その順序に従って，適切なキーの値とする

    if morph.get('base') == '*' : # 未知語について，扱いやすいように必要な情報を付加
        morph['yomi'] = '*'
        morph['oto'] = '*'

    return morph # 得られた辞書型データを返す

if __name__ == '__main__':
    args = sys.argv
    argc = len(args)

    # Check parameter
    if (argc != 2):
        print ('Usage: # python %s file_name' % args[0])
        quit()

    filename = args[1]

    #例えば，品詞情報を用いて，特定の品詞について頻度表を作ってみる
    morph_analysis(filename, 'okurimono_m.txt')
    mlines = get_m_lines('okurimono_m.txt')
    noun_ha(mlines)
