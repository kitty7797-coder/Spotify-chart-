"""
用apify抓剩下的資料
"""
from apify_client import ApifyClient
import pandas as pd
import os
import json

with open('./爬資料/apify_key.json','r')as f:
    content=json.load(f)
    key=content['key']


#匯入資料
ori_data=pd.read_csv('./GAM/2021金曲獎得獎.csv', index_col=False)
# spotify_id=list(ori_data['id'])[::-1]
key_name=list(ori_data['人名'])[::-1]
key_track=list(ori_data['曲目'])[::-1]
full_dict={'name':[], 'href':[],'isrc':[],
           'danceability':[],'energy':[],'instrumentalness':[]
           ,'key':[],'liveness':[],'loudness':[],'mode':[],
           'speechiness':[],'tempo':[],'valence':[]}
canno_find={'name':[]}
# Initialize the ApifyClient with your API token
client = ApifyClient(key)

for _ in range(len(key_track)):
    try:
        # base_input='https://open.spotify.com/track/{}'
        #track_input=base_input.format(spotify_id.pop())
        composer=key_name.pop()
        track_name=key_track.pop()
        
    # Prepare the Actor input
        
        run_input = {
            "tracks": [
                track_name
            ],
            "tracksIncludeArtists": False,
            "tracksIncludeAlbum": False,
            "tracksIncludeAudioFeatures": True,
            "tracksIncludeAvailableMarkets": False,}
        # Run the Actor and wait for it to finish
        run = client.actor("KJEf8oxcDPDjll2BU").call(run_input=run_input)
        
        
        # Fetch and print Actor results from the run's dataset (if there are any)
        for item in client.dataset(run.default_dataset_id).iterate_items():
            features=item['audio_features'][0]
            detail=item['tracks'][0]
        
        #創建字典
        full_dict['name'].append(detail['track_name'])
        full_dict['href'].append(detail['track_url'])
        full_dict['isrc'].append(detail['track_isrc'])
        
        full_dict['danceability'].append(features['track_danceability'])
        full_dict['energy'].append(features['track_energy'])
        full_dict['instrumentalness'].append(features['track_instrumentalness'])
        full_dict['key'].append(features['track_key'])
        full_dict['liveness'].append(features['track_liveness'])
        full_dict['loudness'].append(features['track_loudness'])
        full_dict['mode'].append(features['track_mode'])
        full_dict['speechiness'].append(features['track_speechiness'])
        full_dict['tempo'].append(features['track_tempo'])
        full_dict['valence'].append(features['track_valence'])
    except:
        canno_find['name'].append(detail['track_name'])
        continue
file='./GAM/GAM_music_features'
if not os.path.exists(file):
    os.mkdir(file)

df=pd.DataFrame(full_dict)
df.to_csv(file+'./2021_GAM_music_features.csv', index=False, encoding='utf-8-sig')