from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep
import os
import pandas as pd
# import csv

wrong_data=[]
#打開瀏覽器   
driver=webdriver.Chrome()
#建立資料夾
file_name='./music_feature'
if not os.path.exists(file_name):
    os.mkdir(file_name)

def get_search_id(spotify_id):
    driver.switch_to.window(driver.window_handles[0])
    base_url='https://api.reccobeats.com/v1/track?ids={}'
    search_url=base_url.format(spotify_id)            
    driver.get(search_url)
    driver.implicitly_wait(5) 
    # 獲取內容
    sub_soup=bs(driver.page_source, 'lxml')
    driver.implicitly_wait(5)
    sub_content=sub_soup.find('pre').text
    lst=['{','[','"',':',']','}']
    for i in sub_content:
        if i in lst:
            sub_content=sub_content.replace(i, '/')
        else:
            continue
        
    sub_content=sub_content.split('/')
    for i in sub_content:
        if i=='':
            sub_content.remove(i)
    
    search_id=sub_content[2]
    return search_id
base_url="C:/Users/student/Desktop/Spotify-chart-/uniq_track/{}.csv"
url=base_url.format('2024_uniq_track')
data=pd.read_csv(url, encoding='utf-8-sig')
columns=['uri','track_name']
data.columns=columns

pre_uri=data['uri']
spotify_id=list(map(lambda x:x.split(':').pop(),pre_uri))

search_id=[]
#抓search_id並寫入總表
for _ in range(len(spotify_id)):
    search_id.append(get_search_id(spotify_id.pop()))
data['search_id']=search_id
data.to_csv(url, index=False, encoding='utf-8-sig')
