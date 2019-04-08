import pandas as pd
import io
import os
import sys
import csv
import shutil
import codecs

rawdata_address = 'C:\\Users\\J0116075.JPU\\Desktop\\Merukari\\Data_Korea'

def nakami(read_datafile_name, writefile_name):
  with open(rawdata_address + "\\" + read_datafile_name, 'r', encoding='UTF-8', errors='ignore') as nakami_csv_file:  # encoding='CP932'
    nakami_read_csv_file = csv.reader(nakami_csv_file)
    next(nakami_read_csv_file)
    for row in nakami_read_csv_file:
      item = row[0]
      true_item = item.split('\t')
      # print(true_item)
      # print(true_item[1:])
      for i in true_item[1:]:
        writefile_name.write(i)
        if i == true_item[-1]:
          break
        else:
          writefile_name.write(',')
      writefile_name.write('\n')

    
def header(read_datafile_name, writefile_name):
  count = 1
  with open(rawdata_address + "\\" + read_datafile_name, 'r', encoding='UTF-8', errors='ignore') as header_csv_file:
    header_read_csv_file = csv.reader(header_csv_file)
    for row in header_read_csv_file:
      header_item = row[0]
      true_header_item = header_item.split('\t')
      for i in true_header_item[1:]:
        writefile_name.write(i)
        if i == true_header_item[-1]:
          break
        else:
          writefile_name.write(',')
      writefile_name.write('\n')
      # print(true_header_item[1:])
      count = count + 1
      if count == 2:
        break

def manage(read_datafile_name, remakefile_name):
  with open(rawdata_address + "\\" + remakefile_name, 'w', encoding='UTF-8') as txt_file:
    header(read_datafile_name, txt_file)
    nakami(read_datafile_name, txt_file)
  # os.rename(rawdata_address + "\\" + remakefile_name, 'test.csv')



read_datafile_name = "韓国_2019-02-07.csv"
remakefile_name = "RemakeUTF-8_韓国_2019-02-07.txt"



manage(read_datafile_name, remakefile_name)

df = pd.read_table('RemakeUTF-8_韓国_2019-02-07.txt', delim_whitespace=True)
df.to_csv('RemakeUTF-8_韓国_2019-02-07.csv', index=False)



# header("韓国_2019-02-07.csv")

# nakami("韓国_2019-02-07.csv")
  
  # data_array = [row for row in read_csv_file]
  # # print(data_array)
  # for item in data_array:
  #   true_item = item.split()
  #   print(true_item)




# df_today = pd.read_csv("C:\\Users\\J0116075.JPU\\Desktop\\Merukari\\Data_Korea\\韓国_2019-02-07_A.csv", engine='python', encoding='UTF-8')
# for index_NO_today, data_row_today in df_today.iterrows():
#   print(data_row_today)

  # true_data_row_today = data_row_today.split('\t')
  # print(true_data_row_today)




# df_yesterday = 

# print(df_today)


# overlap_items = []
# for index_NO_today, data_row_today in df_today.iterrows():
#   url_today = data_row_today['url']
#   for index_NO_yesterday, data_row_yesterday in df_yesterday.iterrows():
#     url_yesterday = data_row_yesterday['url']
#     if str(url_today) == str(url_yesterday):
#       overlap_items.append(int(index_NO_today))

# print(len(overlap_items))

# df_today = df_today.drop(overlap_items)
# print(df_today)
# print(len(df_today))
