"""
製作一年的歌曲唯一值
"""
import pandas as pd
import os
import csv

track=set()
#輸入年段
year=eval(input().strip())
mon_lst=['01','02','03','04','05','06','07','08','09','10','11','12']
file_uri='./mon_data/{}/{}{}.csv'
while len(mon_lst)!=0:
    uri=file_uri.format(year, year,mon_lst.pop())
    df=pd.read_csv(uri)
    # df=df.drop(columns='Unnamed: 0.1')
    columns=['index','id','artist_name','track_name','total_stream','total_on+chart']
    df.columns=columns
    df_clean=df[['id','track_name']].dropna()
    pairs = zip(df_clean["id"], df_clean["track_name"])
    track.update(pairs)


file_name='./uniq_track'
if not os.path.exists(file_name):
    os.mkdir(file_name)
with open(file_name+'/2022_uniq_track.csv','w', encoding='utf-8-sig', newline='')as fn:
    writer=csv.writer(fn)
    writer.writerows(i for i in track)
    