"""
製作所有年度的歌曲唯一值
"""
import pandas as pd
import os
import csv


base_url="./uniq_track/{}_uniq_track.csv"
year=input('輸入年度，用/隔開:').split('/')
track=set()
while len(year)!=0:
    url=base_url.format(year.pop())
    df=pd.read_csv(url)
    df.columns=['id','track_name']
    pairs=zip(df["id"], df["track_name"])
    track.update(pairs)
    
    
file_name='./uniq_track'
save_name='/all_uniq_track.csv'
if not os.path.exists(file_name):
    os.mkdir(file_name)
with open(file_name+save_name,'w', encoding='utf-8-sig', newline='')as fn:
    writer=csv.writer(fn)
    writer.writerows(i for i in track)


