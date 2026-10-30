"""
拿取isrc與樂曲長度
"""
import json
import requests
import pandas as pd
import os
import csv
from time import sleep

#因為適用pop最後記得[::-1]翻轉回來
isrcs=[]
release_dates=[]
album_types=[]
duration_ms=[]

#匯入token
with open('spotifyKey.json','r')as f:
    content=json.load(f)
token=content['access_token']

#讀取要要求的id檔案
year=eval(input())
id_url=f'./uniq_track/{year}_uniq_track.2.csv'
id_data=pd.read_csv(id_url, encoding='utf-8-sig')
id_data=id_data.drop(columns=['Unnamed: 4', 'Unnamed: 5'])
#拿取spotify id
spotify_id=list(map(lambda x:x.split(':')[2],  id_data['uri']))
spotify_id=spotify_id[:626]
#開始請求
for _ in range(40):
    now_left=len(spotify_id)
    ids=spotify_id.pop()
    url=f"https://api.spotify.com/v1/tracks/{ids}"
    headers={
        "Authorization": f"Bearer {token}"
        }
    
    response=requests.get(url, headers=headers)
    
    if response.status_code==200:
        track_data=response.json()#獲取音樂資料
        # print(track_data)
    elif response.status_code==429:
        retry_after = int(response.headers.get("Retry-After", 5))
        print(f"達到 Rate Limit，依指示等待 {retry_after} 秒後重試...")
        sleep(retry_after)
    else:
        print(f"請求失敗，狀態碼{response.status_code}")
        print(response.text)
        print(f"到{+now_left}停止運作")
        break
    sleep(0.5)
    #擷取資料    
    isrc=track_data['external_ids']['isrc']#dict
    ms=track_data['duration_ms']#int
    
    if track_data['album']['album_type']=='album':
        album_type='album'
        print("是專輯")
        release_date=track_data['album']['release_date']
    else:
        print('是單曲')
        album_type='single'
        release_date=track_data['album']['release_date']
    
    isrcs.append(isrc)
    duration_ms.append(ms)
    album_types.append(album_type)
    release_dates.append(release_date)
    sleep(1)

new_data=pd.DataFrame({"isrc":isrcs, "release_date":release_date,
                       "album_type":album_type,"duration_ms":duration_ms                       
                       })
#isrc寫入uniq
file="./music_detail"
if not os.path.exists(file):
    os.mkdir(file)
save_name=f"{year}_music_detail.csv"    
if not os.path.exists(file+'/'+save_name):
    print('檔案不存在')
    new_data.to_csv(file+'/'+save_name)
else:
    print('檔案已經存在，用附加模式寫入')
    fn=open(save_name, 'a')
    rows=new_data.values.tolist()
    writer=csv.writer(fn)
    writer.writerows(rows)
    
#isrc，release_date，album_type，duration_ms 另外建一個表格