#### 実行環境
  Windows 10 で動作確認

#### 処理内容
 - メルカリ売上利益ページから売上データを取得

### 使い方
 1. toolsからダウンロードする。
 2. デスクトップ等使いやすいフォルダーに移動する
 3. ダブルクリックして実行する
 4. ブラウザが立ち上がり、ログイン画面が表示されるので、ログインする。
 5. そのまま待機(30分くらいかかるかも)
 6. calcSales.exeと同じフォルダに"salesdata.csv"が出力される

### データ形式
```
['itemId', 'title', 'soldPrice', 'salesFee', 'salesProfit', 'soldTime']
```
 - itemId: 各商品に割り当て割れるID
 - title: 出品したタイトル
 - soldPrice: 売上金
 - salesFee: 手数料(売上金の10％)
 - salesProfit: 販売利益
 - soldTime: 売れた時の値段
