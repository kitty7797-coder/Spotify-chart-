#====================
#   用來將兩週表合併成月表
#   只需要改目標地點即可
#   預設是一年只有兩個月份需要額外處理
#====================
"""
使用前請觀察好合併第一階段完成的檔案!!!
"""
import pandas as pd
import os
import re

country=input('輸入國家:')
year=input('輸入年分:').strip()
except_mon_1=eval(input('輸入三個一組的月份_1(個位數補零):'))
except_mon_2=eval(input('輸入三個一組的月份_2(個位數補零):'))
file_url=f'C:/Users/student/Desktop/Spotify-chart-/all_data/{country}chart/clear_data.2/'
mon=['01','02','03','04','05','06','07','08','09','10','11','12']
#pop掉例外的月份，留最後合併
mon_lst=[mon.pop(except_mon_1-1),mon.pop(except_mon_2-2)]
#記得要改url
while True:
    #輸入第一份資料       
    if len(mon)==0:
        break
    try:
        file_lst=[]
        month=mon.pop()
        #用正則表達式找尋符合的檔案
        pattern=re.compile(rf'^{year}年{month}.*\.csv$')
        for filename in os.listdir(file_url):
            if pattern.match(filename):
                file_lst.append(filename)        
        #讀檔案
        data1=pd.read_csv(file_url+file_lst[0])
        data2=pd.read_csv(file_url+file_lst[1])
                
        clear_pd=pd.merge(data1,data2, on='uri',how='outer')
        data1.info()
        
        #將空的X值填入y的內容 
        clear_pd['artist_names_x']=clear_pd['artist_names_x'].fillna(clear_pd['artist_names_y'])
        clear_pd['track_name_x']=clear_pd['track_name_x'].fillna(clear_pd['track_name_y'])
        clear_pd['total_stream_x']=clear_pd['total_stream_x'].fillna(clear_pd['total_stream_y'])
        #將唯一的streams y設為0方便待會兒相加
        clear_pd['total_stream_y']=clear_pd['total_stream_y'].fillna(0)
        clear_pd['total_stream']=clear_pd['total_stream_x']+clear_pd['total_stream_y']
        clear_pd=clear_pd.drop(columns=['Unnamed: 0_x','Unnamed: 0_y','track_name_y',\
                                        'artist_names_y','total_stream_y',\
                                         'total_stream_x'])
        #把uri清理成只有id
        spotify_id=list(map(lambda x:x.split(':')[2], clear_pd['uri']))    
        clear_pd['uri']=spotify_id
            
        clear_pd.columns=['id','artist_names','track_name','total_stream']
        clear_pd.index=clear_pd.index+1
        
        
        #確認資訊
        clear_pd.info()
        
        file_name=f'C:/Users/student/Desktop/Spotify-chart-/all_data/mon_data_{country}'
        save_name=f'{year}{month}'
        if not os.path.exists(file_name):
            os.mkdir(file_name)
        clear_pd.to_csv(file_name+'/'+save_name+'.csv', encoding='utf-8-sig')
    except Exception as er:
        print(f'沒有這個檔案 or 錯誤原因: {er}')
        continue
           
#處理三個檔案的
file_lst_1=[]
file_lst_2=[]
f_dict={
        0:file_lst_1,
        1:file_lst_2
        }
#用正則表達式找尋符合的檔案
for index,m in enumerate(mon_lst):
    pattern=re.compile(rf'^{year}年{m}.*\.csv$')
    for filename in os.listdir(file_url):
        if pattern.match(filename):
            f_dict[index].append(filename)      
#用concat
for i in [0,1]:
    df_list=[
        pd.read_csv(os.path.join(file_url,f),index_col=False) for f in f_dict[i]
        ]        
            
    if df_list:
        merge_df=pd.concat(df_list, ignore_index=True)
        #把uri清理成只有id
        spotify_id=list(map(lambda x:x.split(':')[2], merge_df['uri']))    
        merge_df['uri']=spotify_id
        #
        merge_df=merge_df.drop(columns=['Unnamed: 0'])    
        merge_df.columns=['id','artist_names','track_name','total_stream']
        merge_df.index=merge_df.index+1
        
        #設定agg規則
        groupby_col=['id']
        sum_col=['total_stream']
        agg_rule={
            col:("sum" if col in sum_col else "first")
            for col in merge_df.columns
            if col not in groupby_col
            }
        #合併並累加stream值
        df=merge_df.groupby(groupby_col, as_index=False).agg(agg_rule)
        name_file=mon_lst[i]        
        save_name=f'{year}{name_file}'
        df.to_csv(file_name+'/'+save_name+'.csv', encoding='utf-8-sig')    
        
        
        
        
        
