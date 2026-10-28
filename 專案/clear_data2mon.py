#====================
#   跟clear_data_2很像
#   只需要改檔案名稱即可
#   另外會有跨越分的週需要額外處理
#====================
import pandas as pd
import os

base_url='C:/Users/student/Desktop/專案/twchart/clear_data/{}年{}，{}月({}).csv'
#記得要改url
while True:
    #輸入第一份資料
    year=input('年:')
    m1=input('月:')
    m2=input('月:')
    num=input('編號:')
    #輸入第二份資料
    year_2=input('年:')
    m1_2=input('月:')
    m2_2=input('月:')
    num_2=input('編號:')
    save_name=input("合併後檔案名稱: ")
    
    file=base_url.format(year,m1,m2,num)
    file2=base_url.format(year_2,m1_2,m2_2,num_2)
    try:
        data1=pd.read_csv(file)
        data2=pd.read_csv(file2)
                
        clear_pd=pd.merge(data1,data2, on='uri',how='outer')
        data1.info()
        
        #將空的X值填入y的內容 
        clear_pd['artist_names_x']=clear_pd['artist_names_x'].fillna(clear_pd['artist_names_y'])
        clear_pd['track_name_x']=clear_pd['track_name_x'].fillna(clear_pd['track_name_y'])
        clear_pd['total_stream_x']=clear_pd['total_stream_x'].fillna(clear_pd['total_stream_y'])
        #將唯一的streams y設為0方便待會兒相加
        clear_pd['total_stream_y']=clear_pd['total_stream_y'].fillna(0)
        clear_pd['total_stream']=clear_pd['total_stream_x']+clear_pd['total_stream_y']
        clear_pd=clear_pd.drop(columns=['Unnamed: 0_x','Unnamed: 0_y','track_name_y','artist_names_y','total_stream_y',\
                                         'total_stream_x'])
        
        clear_pd.columns=['uri','artist_names','track_name','total_stream']
        # #確認資訊
        clear_pd.info()
        
        file_name=f'./mon_data/{year}'
        if not os.path.exists(file_name):
            os.mkdir(file_name)
        clear_pd.to_csv(file_name+'/'+save_name+'.csv', encoding='utf-8-sig')
        break
    except Exception as er:
        print(f'沒有這個檔案 or 錯誤原因: {er}')
        continue
           
