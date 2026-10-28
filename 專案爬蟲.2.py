#===========================================
#      自動下載spotify chart的台灣榜單
#      使用者輸入日期與週數
#      從新到舊自動下載到指定資料夾
#===========================================
from log_IN import LogIN
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import os
import datetime
from datetime import timedelta

#建立datelist
days=[]
weeks=[]
date=input('輸入起始日起，用/隔開: ').strip().split('/')
weeks_num=int(input('抓取週數: ').strip())
date=list(map(lambda i:int(i) , date))
start_day=datetime.date(date[0],date[1],date[2])
days.append(start_day)
while True:
    if len(days)>=weeks_num:
        break    
    new_day=days[-1]-timedelta(days=7)
    days.append(new_day)
day=str(days.pop())

options=webdriver.ChromeOptions()
#建立資料夾
folder_name = "./twchart"
if not os.path.exists(folder_name):
    os.mkdir(folder_name)
#將下載路徑改成資料夾    
download_path=os.path.abspath(folder_name)
prefs={
       'download.default_directory':download_path,
       "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
       }
options.add_experimental_option("prefs", prefs)


#打開瀏覽器至spotify chart, 並將螢幕開全
driver=webdriver.Chrome(options=options)
driver.get('https://charts.spotify.com/charts/view/regional-tw-weekly/latest')
sleep(2)
driver.maximize_window()

#使用class加入cookie
cookie=LogIN(driver)
cookie.import_cookie()
sleep(5)

#到taiwan榜單
driver.get(f'https://charts.spotify.com/charts/view/regional-tw-weekly/{day}')
sleep(3)
#關掉臨時cookie
driver.find_element(By.XPATH, '/html/body/div[2]/div[2]/div/div[2]/button').click()
sleep(1)
#下載
driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div[2]/span/span/button').click()        
sleep(1)
while len(days)!=0:
    day=str(days.pop())
    #到taiwan榜單(如果有起始值，請選擇當月的倒數第二個禮拜)
    driver.get(f'https://charts.spotify.com/charts/view/regional-tw-weekly/{day}')
    sleep(4)
    #下載
    driver.find_element(By.XPATH, '/html/body/div[1]/div/div[3]/div/div/div[2]/span/span/button').click()        
    sleep(3)

print('抓取完成，去看看吧!')