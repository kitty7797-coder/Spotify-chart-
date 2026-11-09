import pandas as pd


year=eval(input())
mon_lst=['01','02','03','04','05','06','07','08','09','10','11','12']
url='./mon_data/{}/{}{}.csv'

while len(mon_lst)!=0:
    new_url=url.format(year,year,mon_lst.pop())
    old_data=pd.read_csv(new_url)
    spotify_id=list(map(lambda x:x.split(':')[2], old_data['uri']))    
    old_data['uri']=spotify_id
    
    old_data.to_csv(new_url, index=False)

print('本年度完成~')