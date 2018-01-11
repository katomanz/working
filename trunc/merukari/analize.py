# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#pd.options.display.mpl_style = 'default'

csv_data  = pd.read_csv('./datum/instagram_2017-12-21.csv')

# Get top brand
# brand_cnt_list = csv_data.groupby('brand')[['url']].count()
# brand_cnt_list = brand_cnt_list.sort_values(by = 'url', ascending=False)

summary_data = csv_data.groupby('brand')[['url']].describe())
print(summary_data
for brand_data in summary_data.groupby('brand')[['url']].describe():
    print(brand_data)

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
