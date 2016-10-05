var client = require('cheerio-httpcli');

/* Sneaker wars */
client.fetch('http://sneakerwars.jp/',
  function (err, $, res, body) {
      // Output Response header
      console.log(res.headers);

      // HTMLタイトルを表示
      console.log($('body').text());

      // リンク一覧を表示
      $('a').each(function (idx) {
          console.log($(this).attr('href'));
      });
});
