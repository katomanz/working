# -*- coding: utf-8 -*-
import MeCab # 必要なモジュールを読み込み
import sys
import string
from collections import OrderedDict

# infileの文章を解析して，結果をoutfileに出力
def morph_analysis(infile, outfile):
    t = MeCab.Tagger(' '.join(sys.argv))
    with open(infile, 'r') as fin:
        with open(outfile, 'w') as fout:
            fout.write(t.parse(fin.read()))
    return outfile

#注　読み込んで解析器に渡し結果を受け取りそれを書き出すまで，すべてutf-8の文字列で行っている
# 解析結果のファイルを読み込む
def get_m_lines(file):
    with open(file, 'r') as f: # 解析結果のファイルを開く
        m_lines = f.read().split('\n') # 読み込んで，改行で分割

        # m_linesの最後2つの要素はEOSと空白なのでカットしておく
        m_lines.pop(-1)
        m_lines.pop(-1)

    return m_lines # 結果（１形態素毎の情報のリスト）を返す

def noun_ha(mlines):
    hist = dict() # キーに名詞、値に頻度（数字）が入るのを想定
    morphs = []
    tr_hist = dict()

    for line in mlines:
        morphs.append(mecab_data(line)) #形態素を１つずつ辞書型に変換

    for i in range(len(morphs) -1): # i+1 が「は」の時を想定しているので、len -1
        #ある形態素の要素が名詞で、その次の要素が係助詞で、かつ係助詞「は」のとき
        if morphs[i]['pos'] == '名詞' \
        and morphs[i+1]['pos1'] == '係助詞' \
        and morphs[i+1]['surface'] == 'は':
            key = morphs[i]['surface'] #その名詞をキーとする
            hist[key] = hist.get(key,0) + 1 #もし、まだそのkeyが存在しなかったら(=初めて出現したら),デフォルト値を0と考えて1を足す。

    for noun in hist: #キーを取り出す
        #histは頻出回数がバリューだが、
        #tr_hist に　頻出回数をキーに変換したものを入れる。バリューを名詞のリストにする
        tr_hist[hist[noun]] = tr_hist.get(hist[noun],[])+[noun]

    #print(tr_hist)
    #{32: ['デラ'], 1: ['呼び鈴', '収入', 'ここ', '違い', '僕', '興奮', 'とき', '時計', '望み', '支出', '答え', 'わたし', 'デザイン', '様子', 'フライパン', 'プレゼント', '文字', '人', '色', '王様', '顔', '表現', '言明', 'たち', '彼', '比喩', '光', '髪の毛', 'セット', 'セント', '小銭', 'わたくし', '彼ら'], 2: ['明日', 'これ', '目', '鎖', '賢者', '宝物', 'の', '一つ'], 3: ['もの', 'こと', 'それ', '主人'], 4: ['髪'], 13: ['ジム']}

    for i in sorted(tr_hist.keys(), reverse = True):
        #見やすく名詞ごとに出力、頻度高い順に
        if i > 1: #頻出回数が2以上なら
            for m in range(len(tr_hist[i])):
                #同じ出現回数の名詞を分けて表示
                print( tr_hist[i][m], i)

# 文字列である解析結果を使いやすい形（辞書型）に
def mecab_data(line):
    #print line #の  助詞,連体化,*,*,*,*,の,ノ,ノ
    mkeys = ['pos', 'pos1', 'pos2', 'pos3', 'inf', 'form', 'base', 'yomi', 'oto'] # キィを定義
    morph = OrderedDict() # 辞書型データの初期化
    data = line.split('\t') # 改行コードを外して(?)，タブで（表記とその他の情報に）分割
    #の 助詞,連体化,*,*,*,*,の,ノ,ノ が、「の」と「助詞,連体化,*,*,*,*,の,ノ,ノ」に分割される
    morph['surface'] = data[0] # 表記をしまう
    #print "===================="
    #print data[0] #な
    #print data[1] #助動詞,*,*,*,特殊・ダ,体言接続,だ,ナ,ナ
    #print "===================="
    features = data[1].split(',') # その他の情報はカンマ区切りなので，カンマで分割 [助詞,連体化,*,*,*,*,の,ノ,ノ]
    for i in range(len(features)) : # 分割されたそれぞれの情報を
        morph[mkeys[i]] = features[i] # その順序に従って，適切なキィの値とする

    if morph.get('base') == '*' : # 未知語について，扱いやすいように必要な情報を付加
        morph['yomi'] = '*'
        morph['oto'] = '*'

    return morph # 得られた辞書型データを返す

#例えば，品詞情報を用いて，特定の品詞について頻度表を作ってみる
morph_analysis('./datum/完売_2018-10-17.txt', 'okurimono_m.txt') #全体の流れ
mlines = get_m_lines('okurimono_m.txt')
morphs_dict = {}
noun_ha(mlines)
