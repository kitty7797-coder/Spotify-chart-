"""
將detail寫入資料庫
"""
import pandas as pd
from sqlalchemy import create_engine

#連接資料庫
engine=create_engine(
       'mysql+pymysql://root:Sql2026kitty@localhost:3306/spotify'
       )
query="SELECT id, spotify_id FROM song"
#抓取檔案
song_id=pd.read_sql(query, con=engine)
#讀detail檔案
data=pd.read_csv('C:/Users/student/Desktop/Spotify-chart-/all_data/music_detail/full_music_detail(2).csv')

new_data=pd.merge(data, song_id, how='inner',on='spotify_id').drop(columns=['track_name'])

new_data=new_data.dropna()
new_data=new_data[['id','spotify_id','isrc','release_date','album_type','duration_ms']]

#整理日期格式
release_date=list(new_data['release_date'])
new_date=[]
for i in release_date:
    new_year=i[:4]
    new_date.append(new_year)
    
new_data['release_date']=new_date


new_data.to_sql(
    name='song_detail',
    con=engine,
    if_exists='append',
    index=False
    )