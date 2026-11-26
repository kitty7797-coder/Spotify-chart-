# -*- coding: utf-8 -*-
"""
做訓練模型，先將排名分類成
"""
#用迴圈找出所有名次，篩選出最高名次抓進表中
import pandas as pd
import datetime
from datetime import timedelta

year=2025

start_time=datetime.date(2025,1,9)
days=[start_time]
while year!=2026:
    new_days=days[-1]+timedelta(days=7)
    days.append(new_days)
    year=new_days.year


train=pd.read_csv('train_data.csv')
test=pd.read_csv('test_data.csv')
rank_lst_id=[]

best_map_id={}
class_map={}

#train
uri='C:/Users/student/Desktop/Spotify-chart-/all_data/tw/twchart/regional-tw-weekly-{}.csv'
for day in days:   
    file_uri=uri.format(day)
    file=pd.read_csv(file_uri)
    id_=list(map(lambda x:x.split(':')[2],file['uri']))
    
    #建立一個新的dataframes
    sub=pd.DataFrame({'id':id_,'rank':file["rank"]}).dropna(subset=['id','rank'])
    sub=sub[sub['id'].isin(test['id'])]
    #篩選同一個id的資料
    for song_id, r in (zip(sub['id'],sub['rank'])):
        if song_id not in best_map_id or r < best_map_id[song_id]:
            best_map_id[song_id]=r
            
            
test['best_rank']=test['id'].map(best_map_id)
for song_id, r in (zip(test['id'],test['best_rank'])):
    if r<=10:
        class_map[song_id]='Top10'    
    elif r<=50:
        class_map[song_id]='Top50'
    elif r<=100:
        class_map[song_id]='Top100'
    elif r<=200:
        class_map[song_id]='Top200'
    
test['class_rank']=test['id'].map(class_map)    
test.to_csv('test_df.csv',encoding='utf-8-sig',index=False)

#music_feature
feature_file=pd.read_csv(
    'C:/Users/student/Desktop/Spotify-chart-/all_data/tw/music_feature/full_music_features.csv'
    )
feature_file['id']=list(map(lambda x:x.split('/')[-1],feature_file['href']))

#合併兩個檔案
#發現當初把重複的isrc刪掉了，我很抱歉QQQQ
df=pd.merge(test, feature_file,how='left',on='id',indicator=True)
df=df[df['_merge']=='both']








  