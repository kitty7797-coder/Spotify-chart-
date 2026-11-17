#====================
#   將兩個檔案合併
#   用outerjoin 集合
#   將相同樂曲的播放量相加
#   weeks_on_chart另外處理
#====================
import pandas as pd
import os
import datetime
from datetime import timedelta

#建立日期清單
days=[]
start_day=datetime.date(2026, 1, 1)
days.append(start_day)
country=input('輸入國家:')
while True:
    if len(days)>=52:
        break    
    new_day=days[-1]-timedelta(days=7)
    days.append(new_day)
while len(days)!=0:
    url=f'C:/Users/student/Desktop/Spotify-chart-/all_data/{country}chart'
    day1=str(days.pop())
    day2=str(days.pop())
    data1=pd.read_csv(url+f'/regional-{country}-weekly-{day1}.csv')  
    data2=pd.read_csv(url+f'/regional-{country}-weekly-{day2}.csv')
    #將不用的欄位drop掉
    data1=data1.drop(columns=['rank','source',\
                              'peak_rank','previous_rank','weeks_on_chart'])
    data2=data2.drop(columns=['rank','source',\
                              'peak_rank','previous_rank','weeks_on_chart'])    
        
    #用外部交集合併兩表
    clear_pd=pd.merge(data1,data2, on='uri',how='outer')
    data1.info()
        
    #將空的X值填入y的內容 
    clear_pd['artist_names_x']=clear_pd['artist_names_x'].fillna(clear_pd['artist_names_y'])
    clear_pd['track_name_x']=clear_pd['track_name_x'].fillna(clear_pd['track_name_y'])
    clear_pd['streams_x']=clear_pd['streams_x'].fillna(clear_pd['streams_y'])
    #將唯一的streams y設為0方便待會兒相加
    clear_pd['streams_y']=clear_pd['streams_y'].fillna(0)
    #相加
    clear_pd['total_stream']=clear_pd['streams_x']+clear_pd['streams_y']
    clear_pd=clear_pd.drop(columns=['track_name_y','artist_names_y',\
                                    'streams_y','streams_x'])
    clear_pd.index=clear_pd.index+1
    #確認資訊
    clear_pd.info()
    #重設欄位名稱
    clear_pd.columns=['uri','artist_names','track_name','total_stream']
    #儲存
    file_name=url+'/clear_data.2/'
    if not os.path.exists(file_name):
        os.mkdir(file_name)
    
    year=day1[0:4]
    mon1=day1[5:7]
    mon2=day2[5:7]
    save_file=file_name+f'{year}年{mon1}，{mon2}月(1).csv'
    if not os.path.exists(save_file):
        clear_pd.to_csv(save_file,encoding='utf-8-sig')
    else:
        clear_pd.to_csv(file_name+f'{year}年{mon1}，{mon2}月(2).csv',encoding='utf-8-sig')