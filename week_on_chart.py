"""
抓week_on_chart最大值
"""
from datetime import timedelta 
import datetime
import pandas as pd

weeks=[]
days=[]
df_onchart=pd.DataFrame({'spotify_id':'','weeks_on_chart':''}, index=[0])

date=input('輸入起始日起，用/隔開: ').strip().split('/')
weeks_num=int(input('抓取週數: ').strip())
date=list(map(lambda i:int(i) , date))
start_day=datetime.date(date[0],date[1],date[2])

days.append(start_day)

while True:
    if len(days)>=weeks_num:
        break
    new_days=days[-1]+timedelta(days=7)
    days.append(new_days)

detail=pd.read_csv('./all_data/uniq_track/all_uniq_track(2).csv')
detail_id=list(detail['id'])

for _ in range(len(days)):
    day=str(days.pop())
    data=pd.read_csv(f'./all_data/twchart/regional-tw-weekly-{day}.csv')
    data['spotify_id']=data['uri'].str[14:]
    df=data[data['spotify_id'].isin(detail_id)]
    df=df[['spotify_id','weeks_on_chart']]    
    df_onchart=pd.concat([df_onchart,df],ignore_index=True)    
    
    
df_onchart.info()    
    
new_df=df_onchart.sort_values('weeks_on_chart', ascending=False).drop_duplicates('spotify_id')   

new_df.to_csv('./new_chart.csv', index=False, encoding='utf-8-sig')

    