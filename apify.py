"""
用apify抓剩下的資料
"""
from apify_client import ApifyClient
import pandas as pd

#匯入資料
ori_data=pd.read_csv('./music_detail/na_left_detail.csv', index_col=False)
spotify_id=list(ori_data['id'])[::-1]
full_dict={'name':[], 'href':[],'isrc':[],
           'daceability':[],'energy':[],'instrumentalness':[]
           ,'key':[],'liveness':[],'loudness':[],'mode':[],
           'speechiness':[],'tempo':[],'valence':[]}
canno_find={'name':[]}
# Initialize the ApifyClient with your API token
client = ApifyClient("apify_api_vGItPi3HtLlvDtn54njuZbXgvv6Igv4BH4iB")

for _ in range(len(spotify_id)):
    try:
        base_input='https://open.spotify.com/track/{}'
        track_input=base_input.format(spotify_id.pop())
    # Prepare the Actor input
        run_input = {
            "tracks": [
                track_input,
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
        
        full_dict['daceability'].append(features['track_danceability'])
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

df=pd.DataFrame(full_dict)
df.to_csv('./music_feature/nan_left_features.csv', index=False, encoding='utf-8-sig')