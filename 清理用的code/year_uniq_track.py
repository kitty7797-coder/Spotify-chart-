"""
製作一年的歌曲唯一值
記得改檔案位置
"""
import pandas as pd
import os
import csv

track=set()
#輸入國家
country=input('請輸入國家:')
#輸入年段
year=eval(input('輸入年分:').strip())
mon_lst=['01','02','03','04','05','06','07','08','09','10','11','12']
file_uri=f'C:/Users/student/Desktop/Spotify-chart-/all_data/{country}/mon_data_{country}'
content_uri='/{}/{}{}.csv'
while len(mon_lst)!=0:
    uri=content_uri.format(year, year,mon_lst.pop())
    df=pd.read_csv(file_uri+uri)
    # df=df.drop(columns='Unnamed: 0.1')
    columns=['index','id','artist_name','track_name','total_stream']
    df.columns=columns
    df_clean=df[['id','track_name']].dropna()
    pairs = zip(df_clean["id"], df_clean["track_name"])
    track.update(pairs)


file_name=f'C:/Users/student/Desktop/Spotify-chart-/all_data/{country}/uniq_track_{country}'
save_name=f'/{year}_uniq_track.csv'
if not os.path.exists(file_name):
    os.mkdir(file_name)
with open(file_name+save_name,'w', encoding='utf-8-sig', newline='')as fn:
    writer=csv.writer(fn)
    writer.writerows(i for i in track)
    