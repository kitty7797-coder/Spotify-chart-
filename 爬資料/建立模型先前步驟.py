# -*- coding: utf-8 -*-
"""
找當初沒有抓到isrc的樂曲
"""
import pandas as pd

full_data=pd.read_csv(
    'C:/Users/student/Desktop/Spotify-chart-/all_data/tw/uniq_track/all_uniq_track(2).csv'
    )

detail_data=pd.read_csv(
    'C:/Users/student/Desktop/Spotify-chart-/all_data/tw/music_detail/full_music_detail(2).csv'
    )

# train_data=pd.read_csv(
#     'C:/Users/student/Desktop/Spotify-chart-/all_data/tw/uniq_track/train_df.csv'
#     )

# full_data['id']=list(map(lambda x:x.split('/')[-1],full_data['href']))


# train_left=pd.merge(train_data, full_data,how='left',on='id',indicator=True)
# train_left=train_left[train_left['_merge']=='left_only']
# train_left=train_left[['id']]

# test_left=pd.merge(test_data, full_data,how='left',on='id',indicator=True)
# test_left=test_left[test_left['_merge']=='left_only']
# test_left=test_left[['id']]

detail_df=pd.merge(detail_data, full_data,how='right',left_on='spotify_id',right_on='id',indicator=True)
detail_df=detail_df[detail_df['_merge']=='right_only']
detail_df=detail_df[['id']]



detail_df.to_csv('id_left_isrc.csv',index=False,encoding='utf-8-sig')
