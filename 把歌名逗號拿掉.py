import pandas as pd

url='./uniq_track/all_uniq_track.csv'
data=pd.read_csv(url)

columns=['id','track_name']
data.columns=columns


name=list(data['track_name'])
new_name=[]


for i in name:
    i=i.replace(',', "")
    new_name.append(i)
            
data['track_name']=new_name

data.to_csv('./uniq_track/all_uniq_track(2).csv', index=False)