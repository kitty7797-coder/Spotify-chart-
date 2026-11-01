from selenium import webdriver
"""
利用search_id來抓音樂特徵
"""
from bs4 import BeautifulSoup as bs
import json
import os
from time import sleep
import pandas as pd
# import csv
url="./music_detail/2023_music_detail.csv"
data=pd.read_csv(url, encoding='utf-8-sig', index_col=False)
search_id=list(data['search_id'])
#因為用pop所以先反過來
search_id=search_id[::-1]
wrong_data=[]
#打開瀏覽器   
driver=webdriver.Chrome()
#建立資料夾
file_name='./music_feature'
if not os.path.exists(file_name):
    os.mkdir(file_name)
    
def get_music_features(search_id):
    #搜尋音樂內容
    base_url='https://api.reccobeats.com/v1/track/{}/audio-features'
    search_url=base_url.format(search_id)
    #前往網址
    driver.get(search_url)
    driver.implicitly_wait(3)
    #解析內容
    soup=bs(driver.page_source, 'lxml')
    driver.implicitly_wait(3)
    content=soup.find('pre').text
    final_content=json.loads(content)
    #利用json.loads直接把string內容轉譯成dict
    driver.implicitly_wait(10) 
    return final_content
    sleep(1)


#抓music_features
final_content=get_music_features(search_id.pop())
df=pd.DataFrame(final_content, index=[0])
for _ in range(len(search_id)):
    try:
        if len(search_id)==0:
            break
        final_content=get_music_features(search_id.pop())
        df.loc[len(df)]=final_content 
        sleep(0.5)
    except Exception as er:
        wrong_data.append(data['track_name'])
        print('錯誤代碼'+er)
        sleep(1)
        df.loc[len(df)]={"id":"","href":"","isrc":"","acousticness":0,"danceability":0,"energy":0,"instrumentalness":0,"key":-1,"liveness":0,"loudness":0,"mode":0,"speechiness":0,"tempo":0,"valence":0}
        continue
#寫入csv檔案
df.index+=1
file_name=os.path.abspath(file_name)
df.to_csv(file_name+'\\2023_music_feature.csv', encoding='utf-8-sig', index=False)  
    
    