import requests
from bs4 import BeautifulSoup as bp
import csv

url='https://www.bamid.gov.tw/News_Content.aspx?n=3539&s=124254'
req=requests.get(url)
soup=bp(req.text, 'lxml')
content_lst=[]

content=soup.find('div', {'id':'CCMS_Content'}).find_all('p')

for i in content:
    content_lst.append([i.text])


with open('./GAM/2021金曲獎提名(x).csv', 'w')as f:
    writer=csv.writer(f)    
    writer.writerow(content_lst)