import pandas as pd

url='./music_detail/2023_music_detail(2).csv'
data=pd.read_csv(url)

name=list(data['track_name'])
new_name=[]


for i in name:
    i=i.replace(',', "")
    new_name.append(i)
            
data['track_name']=new_name

data.to_csv('./music_detail/2023_music_detail(3).csv', index=False)