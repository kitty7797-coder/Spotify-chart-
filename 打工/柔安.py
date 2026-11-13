"""
Created on Thu Nov 12 21:04:25 2026

@author: shaoK
"""
import pandas as pd

data1=pd.read_excel('課照中心(全).xlsx')
data2=pd.read_excel('單位清冊(兒童課後照顧服務中心+補習班).xlsx')
data3=pd.read_csv('補習班(全).csv')

#增加類別值
data1['類別']='兒童課後照顧服務中心'
data3['類別']='補習班'

data2.columns=data2.iloc[0,0:9]
data2=data2.drop(0)
data3=data3.iloc[:,0:8]


data1.columns=[95,'單位名稱','郵遞區號','里別','鄰','郵遞區號3+2','地址','電話','負責人','類別']
data2.columns=['類別','行政區','單位名稱','地址','帳號數','班級數','清查結果(續用/停用)','備註事項']
data3.columns=['補習班序號','主管機關文件代碼','補習班中文名稱','補習班中文住址','設立人','立案日期','立案文號','類別']


#把台變成臺
data1['地址']=data1['地址'].str.replace('台','臺')
data2['地址']=data2['地址'].str.replace('台','臺')
data3['補習班中文住址']=data3['補習班中文住址'].str.replace('台','臺')
#清理兩邊空值

data1['地址']=data1['地址'].str.strip()
data2['地址']=data2['地址'].str.strip()
data3['補習班中文住址']=data3['補習班中文住址'].str.strip()

#找出沒有臺北市三個字的重新填回去
new_address_data2_1=[]
new_address_data2_2=[]
new_address_data3_1=[]
for j,k in enumerate(data2['地址']):
    j+=1
    if '區' not in k:
        k=data2['行政區'][j]+k
    elif data2['行政區'][j] not in k:
        k=k[3:]
        k=data2['行政區'][j]+k
    new_address_data2_1.append(k)
    
data2['地址']=new_address_data2_1
for i in new_address_data2_1:
    if '臺北市'not in i:
        i='臺北市'+i
    new_address_data2_2.append(i)
data2['地址']=new_address_data2_2
    
for i in data3['補習班中文住址']:
    i=i[3:]
    if '臺北市'not in i:
        i='臺北市'+i
    new_address_data3_1.append(i)    
data3['補習班中文住址']=new_address_data3_1
#查看
data1.info()
data2.info()
data3.info()

#先篩選課照中心
df_care=pd.merge(data1,data2,how="inner",on=['地址','類別'])
#篩選補習班
df_teach=pd.merge(data2,data3,how="inner",right_on=['補習班中文住址','類別'],left_on=['地址','類別'])
#保留原本欄位
df_care=df_care[['類別','行政區','單位名稱_x','地址','帳號數','班級數','清查結果(續用/停用)','備註事項']]
df_care=df_care.rename(columns={'單位名稱_x':'單位名稱'})
df_teach=df_teach[['類別','行政區','單位名稱','地址','帳號數','班級數','清查結果(續用/停用)','備註事項']]

df_new=pd.concat([df_care,df_teach],ignore_index=True)

df_new.info()


df=pd.merge(df_new, data2, how='inner',on=['地址','類別'],indicator=True)


df_new.to_csv('./存活的資料.csv',index=False, encoding='utf-8-sig')





