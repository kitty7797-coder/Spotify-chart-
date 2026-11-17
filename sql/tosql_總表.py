"""
將總表寫入資料庫
"""
import pandas as pd
from sqlalchemy import create_engine

engine=create_engine(
    'mysql+pymysql://root:Sql2026kitty@localhost:3306/spotify')

data=pd.read_csv('C:/Users/student/Desktop/Spotify-chart-/all_data/uniq_track/all_uniq_track.csv')
columns=['spotify_id','track_name']
data.columns=columns

data.to_sql(
    name='song',
    con=engine,
    if_exists='fail',
    index=False
    
    )