from selenium import webdriver
from bs4 import BeautifulSoup as bs
import json
from time import sleep
import os
import pandas as pd

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
    sleep(2)
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
    driver.implicitly_wait(3)
    # 使用window.open()在目前的瀏覽器新開一個分頁
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[1])
    driver.implicitly_wait(3)# 切換至新開分頁
    driver.get(search_url)
    sleep(3)# 開啟第二個頁面 - 搜尋介面
    #解析內容
    soup=bs(driver.page_source, 'lxml')
    content=soup.find('pre').text
    final_content=json.loads(content)
    #利用json.loads直接把string內容轉譯成dict
    driver.implicitly_wait(10) 
    driver.close()
    return final_content

base_url="C:/Users/student/Desktop/Spotify-chart-/mon_data/2024/{}.csv"
url=base_url.format('2024-2')
data=pd.read_csv(url)

pre_uri=data['uri']
spotify_id=list(map(lambda x:x.split(':').pop(),pre_uri))

final_content=get_search_id(spotify_id.pop())
df=pd.DataFrame(final_content, index=[0])

for _ in range(len(spotify_id)):
    try:
        if len(spotify_id)==0:
            break
        final_content=get_search_id(spotify_id.pop())
        df.loc[len(df)]=final_content
        
        
    except Exception as er:
        wrong_data.append(er)
        driver.implicitly_wait(10)
        df.loc[len(df)]={"id":"","href":"","isrc":"","acousticness":0,"danceability":0,"energy":0,"instrumentalness":0,"key":-1,"liveness":0,"loudness":0,"mode":0,"speechiness":0,"tempo":0,"valence":0}
        driver.close()
        continue
#寫入csv檔案
df.index+=1
file_name=os.path.abspath(file_name)
df.to_csv(file_name+'\\2024_music_feature_2.csv', encoding='utf-8-sig')  
    
    