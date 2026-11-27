# -*- coding: utf-8 -*-
"""
拉出兩個detail表，合併查找isrc，再用isrc去找misic_feature
"""
#拿所有isrc
import pandas as pd

full_detail=pd.read_csv(
    'C:/Users/student/Desktop/Spotify-chart-/all_data/tw/music_detail/full_music_detail(2).csv'
    )
left_detail=pd.read_csv(
    'C:/Users/student/Desktop/Spotify-chart-/all_data/tw/music_detail/left_get_data.csv'
    )

full_detail=full_detail.rename(columns={'spotify_id':'id'})

merge_ft=pd.concat([full_detail,left_detail],ignore_index=True)

#把train,test拉進來
train_data=pd.read_csv(
    './train_df.csv'   
    )
test_data=pd.read_csv('./test_df.csv')
#先找test的所有isrc+刪掉缺值
test_isrc=pd.merge(test_data, merge_ft,how='left',on='id',indicator=True).dropna()
check_isrc=test_isrc[test_isrc['_merge']!='both']
#指留右表的isrc
test_isrc.info()
test_isrc=test_isrc.drop(columns=['release_date','album_type','duration_ms','_merge'])

#==========================================================
#找train的
train_isrc=pd.merge(train_data,merge_ft,how='left',on='id',indicator=True).dropna()
check_isrc=train_isrc[train_isrc['_merge']!='both']

#指留右表的isrc
train_isrc=train_isrc.drop(columns=['release_date','album_type','duration_ms','_merge'])

#先匯出兩表
train_isrc.to_csv('train_isrc.csv',encoding='utf-8-sig',index=False)
test_isrc.to_csv('test_isrc.csv',encoding='utf-8-sig',index=False)






















