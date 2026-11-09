import pandas as pd


# year=eval(input())
mon_lst=['2023','2024','2025']
url='./uniq_track/{}_uniq_track.csv'

while len(mon_lst)!=0:
    new_url=url.format(mon_lst.pop())
    old_data=pd.read_csv(new_url)
    spotify_id=list(map(lambda x:x.split(':')[2], old_data['uri']))    
    old_data['uri']=spotify_id
    
    old_data.to_csv(new_url, index=False)

print('本資料完成~')