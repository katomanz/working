import mysql.connector
import datetime

db_settings = {
     "database":"wordpressdb",
     "host":"160.16.116.29",
     "user":"katomanz",
     "password":"wonbin8083",
     "port":3306,
     "charset":"utf8"
 }

conn = mysql.connector.connect(**db_settings)
cur = conn.cursor()

conn2 = mysql.connector.connect(**db_settings)
cur2 = conn2.cursor()

conn3 = mysql.connector.connect(**db_settings)
cur3 = conn3.cursor()

cur.execute("SELECT url FROM wp_merukari_sales_data")
for url in cur:
    cur2.execute("SELECT post_timestamp FROM wp_merukari_sales_data WHERE url=%s", url)
    httpdate = str(cur2.fetchone())
    _url =  str(url)
    if(len(httpdate) > 29):
        datetime_format = datetime.datetime.strptime(httpdate[2:-3], '%a, %d %b %Y %H:%M:%S GMT')
        cur3.execute("UPDATE wp_merukari_sales_data SET post_timestamp=%s WHERE url=%s", (str(datetime_format), _url[2:-3]))
        print("UPDATE wp_merukari_sales_data SET post_timestamp='{0}' WHERE url='{1}'".format(str(datetime_format), _url[2:-3]), file=codecs.open('gorilla.txt', 'a', 'utf-8'))
        