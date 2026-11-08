#=================
#  因為有空值才又寫了一個
#  抓全部請用.2的檔案
#=================

from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep

data=pd.read_csv('./music_detail/left_music_detail.csv', index_col=False)
filter_data=data[data['search_id'].isna()]
data=data.dropna()


filter_data.to_csv('./music_detail/na_left_detail.csv', index=False, encoding='utf-8-sig')
data.to_csv('./music_detail/left_music_detail(2).csv', index=False, encoding='utf-8-sig')