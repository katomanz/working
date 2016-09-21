// モジュール読み込み
var client = require('cheerio-httpcli');
var url = 'http://rei19.hatenablog.com/archive/2013';
// スクレイピング開始
client.fetch(url,{}, function (err, $, res) {
  // 記事のタイトルを取得
  $('.entry-title-link').each(function() {
    console.log($(this).text());
  });
});

var express = require('express');
var app = express();

app.get('/', function (req, res) {
  res.send('Hello, World!');
});

app.listen(3000);
