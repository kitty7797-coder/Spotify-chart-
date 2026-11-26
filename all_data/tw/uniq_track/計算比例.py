# -*- coding: utf-8 -*-
"""
Created on Thu Nov 26 09:37:08 2026

@author: student
"""
import pandas as pd
import matplotlib.pyplot as plt

data1=pd.read_csv('2021_uniq_track.csv')
data2=pd.read_csv('2022_uniq_track.csv')
data3=pd.read_csv('2023_uniq_track.csv')
data4=pd.read_csv('2024_uniq_track.csv')

test=pd.read_csv('2025_uniq_track.csv')


train=pd.concat([data1,data2,data3,data4],ignore_index=True)
groupby_col=['id']

test_df=pd.merge(test, train,how='left',on='id',indicator=True)
test_df=test_df[test_df["_merge"]=='left_only'].drop(columns=['_merge','track_name_y'])


train_df=train.drop_duplicates(subset=['id'])

#畫圓餅圖
labels=['train','test']
sizes=[2795,566]

plt.pie(sizes,labels=labels,autopct='%1.1f%%',startangle=90)

plt.axis('equal')
plt.title('訓練檔與測試檔的比例')

#輸出訓練集與測試集
test_df.to_csv('test_data.csv',index=False)
train_df.to_csv('train_data.csv',index=False)








