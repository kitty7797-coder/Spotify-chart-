import pandas as pd

url='./music_feature/full_music_features.csv'
data=pd.read_csv(url)

data=data.drop_duplicates(subset=['isrc'])
data=data.drop(columns=['name'])

name=list(data['track_name'])
new_name=[]


for i in name:
    i=i.replace(',', "")
    new_name.append(i)
            
data['track_name']=new_name

data.to_csv('./music_feature/full_music_features.csv', index=False,encoding='utf-8-sig')