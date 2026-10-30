"""
spotify API Client Credentials Flow
每60分鐘更新，使用前記得要來重新跑
"""
import json
import base64
import requests

with open('spotifyKey.json','r', encoding='utf-8')as f:
    content=json.load(f)
    
    client_id=content['client_id']
    client_secret=content['client_secret']
    credentials=f'{client_id}:{client_secret}'
#重新編碼再解碼，拿這個碼才可以去換access token
encoded_credentials=base64.b64encode(credentials.encode('utf-8')).decode("utf-8")

#設定好header 和 data格式
url="https://accounts.spotify.com/api/token"
headers = {"Authorization": f"Basic {encoded_credentials}"}
data={"grant_type": "client_credentials"}

#發出請求
response=requests.post(url, headers=headers, data=data)

if response.status_code==200:
    body=response.json()
    token=body.get('access_token')
    print(token)
    
content['access_token']=token
with open('spotifyKey.json','w', encoding='utf-8')as fn:
    json.dump(content, fn, ensure_ascii=False, indent=4)
