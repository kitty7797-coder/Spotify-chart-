"""
整理60個表
"""
import pandas as pd
from sqlalchemy import create_engine

#連接資料庫
engine=create_engine(
       'mysql+pymysql://root:kittysql77@localhost:3306/spotify'
       )
query="SELECT id, spotify_id FROM song"
#抓取檔案
song_id=pd.read_sql(query, con=engine)
#讀取檔案
year=2022
while year!=2026:
    mon=['01','02','03','04','05','06','07','08','09','10','11','12']
    for index,m in enumerate(mon):
        url=f'./mon_data/{year}/{year}{m}.csv'
        try:
            data1=pd.read_csv(url, index_col=False)
        except:
            print(f'{url}找不到檔案')
            continue
        data1.rename(columns={'uri':'spotify_id'}, inplace=True)
        #合併id
        new_data=pd.merge(data1, song_id, how='inner',on='spotify_id')
        new_data=new_data.drop(columns=['Unnamed: 0', 'artist_names', 'track_name'])
        new_data=new_data[['id','spotify_id','total_stream','total_on_chart']]
        date_num=f'{year}-{index+1}-01'
        new_data['date']=date_num
        #寫入資料庫
        new_data.to_sql(
            name='year_chart',
            con=engine,
            if_exists='append',
            index=False
            )
    year+=1