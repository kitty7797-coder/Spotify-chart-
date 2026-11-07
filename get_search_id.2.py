from selenium import webdriver
from bs4 import BeautifulSoup as bs
import pandas as pd
from time import sleep

wrong_data=[]
#打開瀏覽器   
driver=webdriver.Chrome()
#建立資料夾
# file_name='./music_feature'
# if not os.path.exists(file_name):
#     os.mkdir(file_name)

def get_search_id(track_isrc):
    driver.switch_to.window(driver.window_handles[0])
    base_url='https://api.reccobeats.com/v1/track?ids={}'
    search_url=base_url.format(track_isrc)            
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
    
year=input('輸入檔案名稱:')
url=f"./music_detail/{year}_music_detail.csv"
data=pd.read_csv(url, encoding='utf-8-sig', index_col=False)


track_isrc=list(data['isrc'])
track_isrc=track_isrc[::-1]
search_id=[]
#抓search_id並寫入總表
for _ in range(len(track_isrc)):
    search_id.append(get_search_id(track_isrc.pop()))
    sleep(2)
data['search_id']=search_id
data.to_csv(url, index=False, encoding='utf-8-sig')
