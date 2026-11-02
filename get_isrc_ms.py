"""
拿取isrc與樂曲長度
"""
import json
import requests
import pandas as pd
import os
import csv
from time import sleep

#因為是用pop最後記得[::-1]翻轉回來
isrcs=[]
release_dates=[]
album_types=[]
duration_ms=[]
wrong_name=[]
track_name=[]
track_id=[]
#匯入token
with open('spotifyKey.json','r')as f:
    content=json.load(f)
token=content['access_token']

#讀取要要求的id檔案
year=input()
id_url=f'./uniq_track/{year}_uniq_track.csv'
id_data=pd.read_csv(id_url, encoding='utf-8-sig')
columns=['id','track_name']
id_data.columns=columns
spotify_id=list(id_data['id'])
spotify_id=spotify_id[:1752]
order=0
now_left=len(spotify_id)
#開始請求
while len(spotify_id)!=0:
    
    if order=='88888888':
        print('先休息一下')
        break
    for _ in range(40):        
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
            print(f"到{+now_left}停止運作")
            break
        else:
            print(f"請求失敗，狀態碼{response.status_code}")
            print(response.text)
            print(f"到{+now_left}停止運作")
            break
        sleep(1)
        #擷取資料
        if not track_data['external_ids']['isrc']:
            wrong_name.append(track_data['name'])
            isrc=ids
        elif not track_data['duration_ms']:
            wrong_name.append(track_data['name'])
            ms=''
        else:
            isrc=track_data['external_ids']['isrc']
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
        track_name.append(track_data['name'])
        track_id.append(track_data['id'])
        sleep(3)
    
        new_data=pd.DataFrame({"id":track_id,"track_name":track_name,
                               "isrc":isrcs, "release_date":release_dates,
                               "album_type":album_types,"duration_ms":duration_ms,
                               
                               })
    now_left=len(spotify_id)
    print(f'還剩下{now_left}個檔案')
    order=input("隨意輸入數字，這是用來讓迴圈不會走太快，八個八結束迴圈:")    
#isrc寫入uniq
file="./music_detail"
if not os.path.exists(file):
    os.mkdir(file)
save_name="left_music_detail.csv"    
if not os.path.exists(file+'/'+save_name):
    print('檔案不存在')
    new_data.to_csv(file+'/'+save_name, index=False)
else:
    print('檔案已經存在，用附加模式寫入')
    fn=open(file+'/'+save_name, 'a', newline='')
    rows=new_data.values.tolist()
    writer=csv.writer(fn)
    writer.writerows(rows)
    fn.close()
#isrc，release_date，album_type，duration_ms 另外建一個表格