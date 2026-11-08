import pandas as pd

data2023=pd.read_csv('./music_feature/2023_music_feature(2).csv')
dataleft=pd.read_csv('./music_feature/left_music_feature.csv')
datana=pd.read_csv('./music_feature/nan_left_features.csv')

data2023=data2023.drop(columns=['acousticness','id'])
dataleft=dataleft.drop(columns=['acousticness','id'])
datana=datana.drop(columns=['name'])
datana.rename(columns={'daceability':'danceability'}, inplace=True)

full_data=pd.concat([datana, dataleft, data2023])

real_data=full_data.drop_duplicates()

