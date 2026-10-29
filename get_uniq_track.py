"""
製作一年的歌曲唯一值
"""
import pandas as pd
import os
import csv

track=set()
#輸入年段
year=eval(input().strip())
file_uri='./mon_data/{}/{}-{}.csv'
for i in range(1,13):
    uri=file_uri.format(year, year,str(i))
    df=pd.read_csv(uri)
    columns=['index','uri','artist_name','track_name','total_stream']
    df.columns=columns
    df_clean=df[['uri','track_name']].dropna()
    pairs = zip(df_clean["uri"], df_clean["track_name"])
    track.update(pairs)



file_name='./uniq_track'
if not os.path.exists(file_name):
    os.mkdir(file_name)
with open(file_name+'/2025_uniq_track.csv','w', encoding='utf-8-sig', newline='')as fn:
    writer=csv.writer(fn)
    writer.writerows(i for i in track)
    