#### 実行環境
  Ubuntu 16.04 以上で動作確認
#### 実行方法
```
$ python3.x getSellsData.py　Keyword
```
python 3.6 で動作確認。

#### 処理内容
 - メルカリでKeywordの検索をかけて、結果をCSVファイルで出力する(sclpMerukari/merukari.py)
 - 出力結果(CSV or html)をGoogle Driveに保存する(dataUpload/dataUpload.py)
 - ちょっとした解析する、解析結果はhtmlファイル(analize/analize.py)
 - LINEで通知、通知先は登録している宛先のみ(notification.py)

#### セットアップ
1. Google Chrome Driver のインストールと設置
1. pip install で必要ライブラリのインストール
```
$ pip3 install -r requirement.txt
```
1. Google Driveの認証設定
1. LINE Notifyの認証設定
1. .bashrcに環境変数の設定

```
export GOOGLEDRV_FLDR_ID="FILEWOAGETAI_GOOGLEDRIVENOFOLDERID"
export LINE_NOTIFY_TOKEN="NINSYOUPAGEDE_DETEKITA_LINE_TOKEN"
```
#### 設定/出力結果
- sclpMerukari/merukari.pyを編集すること検索条件を編集可能。
- 現在指定されている設定は以下。
  - カテゴリの指定(デフォルト値: メンズ)
  - 売買金額下限(デフォルト値: 3000円)
  - 商品の状態(デフォルト値: 新品未使用)
  - 売り切れ商品かどうか(デフォルト値: 売り切れ)
- 出力結果ファイル名:「検索ワード_検索日.csv」
- 出力場所: "/datum"
- メルカリ検索ページの20ページ分(900件弱)のデータを抽出
