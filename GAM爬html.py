import pandas as pd
from bs4 import BeautifulSoup as bp

file=open('2024-name.html')
soup=bp(file,'html.parser' )
content=soup.find_all('span')
content_lst=[]
for i in content:
    content_lst.append(i.text)

content_lst=list(map(lambda x: x.strip(), content_lst))    
content_lst=list(filter(lambda x: x!='', content_lst))

for index,m in enumerate(content_lst):
    try:
        if m[:5]==content_lst[index+1][:5]:
            content_lst.remove(m)
    except:
        continue
    
content_str=''.join(content_lst)
    
content_str=content_str.split('■')
new_data=list(map(lambda x:x.split('／'), content_str))

df=pd.DataFrame(new_data)
drop_lst=[i for i in range(7,50,2)]

df=df.drop(index=drop_lst)
df.to_csv('./GAM/2024金曲獎提名.CSV',encoding='utf-8-sig')

file.close()