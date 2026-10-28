import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup as bs


data=pd.read_csv('C:/Users/student/Desktop/專案/mon_data/2024/2024-1.csv')
uri_list=list(map(lambda i:i.split(':'),data['uri']))
spotify_id=uri_list[0][2]
base_url='https://api.reccobeats.com/v1/track?ids={}'

search_url=base_url.format(spotify_id)

driver=webdriver.Chrome()
driver.get(search_url)

# page=driver.page_source
soup=bs(driver.page_source, 'lxml')
content=soup.find('pre').text
lst=['{','[','"',':',']','}']
for i in content:
    if i in lst:
        content=content.replace(i, '/')
    else:
        continue
    
content=content.split('/')
for i in content:
    if i=='':
        content.remove(i)

search_id=content[2]

