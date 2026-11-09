import pandas as pd

data2023=pd.read_csv('./music_feature/2023_music_feature(2).csv')
dataleft=pd.read_csv('./music_feature/left_music_feature.csv')
datana=pd.read_csv('./music_feature/nan_left_features.csv')
datafilter=pd.read_csv('./music_feature/filter_music_features.csv')
datauniq=pd.read_csv('./uniq_track/all_uniq_track(2).csv')
data=pd.read_csv('./music_detail/full_music_detail(2).csv')

data2023=data2023.drop(columns=['acousticness','id'])
dataleft=dataleft.drop(columns=['acousticness','id'])
# datana=datana.drop(columns=['name'])
# datafilter=datafilter.drop(columns=['name'])


data.rename(columns={'id':'spotify_id'}, inplace=True)

full_data=pd.concat([datana, dataleft, data2023, datafilter])

real_data=full_data.drop_duplicates(subset=['isrc'])
data=data.drop_duplicates(subset=['isrc'])

data.to_csv('./music_detail/full_music_detail(2).csv', index=False, encoding='utf-8-sig')

#找缺值
got=pd.merge(data, real_data, how='outer', on='isrc', indicator=True)
got=got[got['_merge']!='both']

