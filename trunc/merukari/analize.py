# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
#import matplotlib.pyplot as plt
#pd.options.display.mpl_style = 'default'

### string
stringForLink="<a href=\"replace\" target=\"_blank\">replace2</a>"

csv_data = pd.read_table('./datum/韓国_2018-04-27.csv')
csv_data.fillna('No Brand', inplace=True)

csv_data['brand-sub_sub_category'] = csv_data['brand'] + ' + ' +csv_data['sub_sub_category']
vc = csv_data['brand-sub_sub_category'].value_counts(dropna=False)
vc.columns = ['brand-sub_sub_category', 'count']
i = 0
htmlData = pd.DataFrame()
for index_name, item in vc.iteritems():
    htmlData.append(csv_data[csv_data['brand-sub_sub_category'] == index_name])
    if i == 2:
        break
    i = i + 1

# Delete unnecessary columns
del htmlData['sub_category']
del htmlData['brand']
del htmlData['sold']

test.to_html('sample.html')

# Get top brand
# brand_cnt_list = csv_data.groupby('brand')[['url']].count()
# brand_cnt_list = brand_cnt_list.sort_values(by = 'url', ascending=False)

#summary_data = csv_data.groupby('brand')[['url']].describe()
#print(summary_data)
#for brand_data in summary_data.groupby('brand')[['url']].describe():
#    print(brand_data)

#print(brand_cnt)
# brand_df = pd.DataFrame(brand_cnt, columns = ['count'])
# print(brand_df)

# brand_df = brand_df.sort_values(by = 'count')

# print(brand_df)

# TODO: Sort list by count
#print(csv_data.groupby('brand')[['price']].sort(columns='brand', ascending=True))


# TODO: Get the most brand
#print(csv_data.groupby('brand')[['price']].count())

# TODO: Check the sub_category

# TODO: Check the price
