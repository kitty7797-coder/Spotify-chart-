import pandas as pd

with open('./GAM/2021金曲獎提名(x).CSV',encoding='utf-8-sig')as f:
    data=f.read()
    

data=data.split('■')
new_data=list(map(lambda x:x.split('／'), data))

df=pd.DataFrame(new_data)


df.to_csv('./GAM/2021金曲獎提名.CSV',encoding='utf-8-sig')