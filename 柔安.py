"""
Created on Thu Nov 12 21:04:25 2026

@author: shaoK
"""
import pandas as pd

data1=pd.read_excel('課照中心(全).xlsx')
data2=pd.read_excel('單位清冊(兒童課後照顧服務中心+補習班).xlsx')
data3=pd.read_csv('補習班(全).csv')

data2.columns=data2.iloc[0,0:9]
data2=data2.drop(0)
data3=data3.iloc[:,0:7]

data1.info()
data2.info()
data3.info()