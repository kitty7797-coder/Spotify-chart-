"""
將新的on_chart寫入資料庫
"""
import pandas as pd
from sqlalchemy import create_engine

engine=create_engine(
       'mysql+pymysql://root:Sql2026kitty@localhost:3306/spotify'
       )
query="SELECT id, spotify_id FROM song"
song_id=pd.read_sql(query, con=engine)
#檔案
data=pd.read_csv('C:/Users/student/Desktop/Spotify-chart-/all_data/new_chart.csv')

new_data=pd.merge(song_id,data,how='inner',on='spotify_id').drop(columns=['spotify_id'])

new_data.to_sql(
    name='weeks_on_chart',
    con=engine,
    if_exists='append',
    index=False
    )