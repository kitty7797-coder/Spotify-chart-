"""
將features寫入資料庫
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
#讀features檔案
data=pd.read_csv('C:/Users/student/Desktop/Spotify-chart-/all_data/music_feature/full_music_features.csv')

data.to_sql(
    name='song_features',
    con=engine,
    if_exists='append',
    index=False
    )