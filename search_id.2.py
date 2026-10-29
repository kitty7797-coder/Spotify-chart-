from selenium import webdriver
from bs4 import BeautifulSoup as bs
import json
from time import sleep
import os
import pandas as pd
import csv
 
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
    sleep(1)
    # 獲取內容
    sub_soup=bs(driver.page_source, 'lxml')
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
    final_content=get_music_features(search_id)
    return final_content
    
def get_music_features(search_id):
    #搜尋音樂內容
    base_url='https://api.reccobeats.com/v1/track/{}/audio-features'
    search_url=base_url.format(search_id)
    # 使用window.open()在目前的瀏覽器新開一個分頁
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])  # 切換至新開分頁
    driver.get(search_url)# 開啟第二個頁面 - 搜尋介面
    #解析內容
    soup=bs(driver.page_source, 'lxml')
    content=soup.find('pre').text
    final_content=json.loads(content)
    #利用json.loads直接把string內容轉譯成dict
    sleep(3)
    driver.close()
    return final_content

base_url="C:/Users/student/Desktop/Spotify-chart-/mon_data/2024/{}.csv"
url=base_url.format('2024-1')
data=pd.read_csv(url)

pre_uri=data['uri']
spotify_id=list(map(lambda x:x.split(':').pop(),pre_uri))

final_content=get_search_id(spotify_id.pop())
df=pd.DataFrame(final_content, index=[0])

# file.to_csv(file_name+'/2024_music_feature.csv', encoding='utf-8-sig')

# fn=open('2024_music_feature.csv', 'w', newline='')
# writer=csv.writer(fn)
for i in spotify_id:
    final_content=get_search_id(i)
    df.loc[len(df)]=final_content
    
    
    
    