"""
Created on Fri Nov 13 13:57:33 2026

@author: student
"""
import pandas as pd

data=pd.read_csv('./存活的資料.csv')
data2=pd.read_excel('./單位清冊(兒童課後照顧服務中心+補習班).xlsx')
data2=data2.drop(0)

data2.columns=['類別','行政區','單位名稱','地址','帳號數','班級數','清查結果(續用/停用)','備註事項']


data2['地址']=data2['地址'].str.replace('台','臺')
data2['地址']=data2['地址'].str.strip()

new_address_data2_1=[]
new_address_data2_2=[]

for j,k in enumerate(data2['地址']):
    if '區' not in k:
        k=data2['行政區'][j]+k
    new_address_data2_1.append(k)
    
data2['地址']=new_address_data2_1
for i in new_address_data2_1:
    if '臺北市'not in i:
        i='臺北市'+i
    new_address_data2_2.append(i)
data2['地址']=new_address_data2_2
du=data2[data2.duplicated(subset=['地址', '類別'], keep=False)]


df=pd.merge(data, data2, how='inner',on=['地址','類別'],indicator=True)
du.to_csv('./我問號.csv')