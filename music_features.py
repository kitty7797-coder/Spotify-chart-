from selenium import webdriver
from bs4 import BeautifulSoup as bs
import json
import os
from time import sleep
import pandas as pd
# import csv
base_url="C:/Users/student/Desktop/Spotify-chart-/uniq_track/{}.csv"
url=base_url.format('2023_uniq_track')
data=pd.read_csv(url, encoding='utf-8-sig')
search_id=list(data['search_id'])
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


#抓music_features
final_content=get_music_features(search_id.pop())
df=pd.DataFrame(final_content, index=[0])
for _ in range(len(search_id)):
    try:
        if len(search_id)==0:
            break
        final_content=get_music_features(search_id.pop())
        df.loc[len(df)]=final_content       
    except Exception as er:
        wrong_data.append(er)
        sleep(3)
        df.loc[len(df)]={"id":"","href":"","isrc":"","acousticness":0,"danceability":0,"energy":0,"instrumentalness":0,"key":-1,"liveness":0,"loudness":0,"mode":0,"speechiness":0,"tempo":0,"valence":0}
        continue
#寫入csv檔案
df.index+=1
file_name=os.path.abspath(file_name)
df.to_csv(file_name+'\\2023_music_feature.csv', encoding='utf-8-sig')  
    
    