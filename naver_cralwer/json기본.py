# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 14:10:57 2019

@author: sec
"""

import requests 
import json

# 네이버 뉴스 url을 입력합니다.
url="https://news.naver.com/main/read.nhn?m_view=1&includeAllCount=true&mode=LSD&mid=shm&sid1=100&oid=001&aid=0000000001" 

oid=url.split("oid=")[1].split("&")[0] 
aid=url.split("aid=")[1] 
page=1 
header = { 
    "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", 
    "referer":url, 
}  

c_url="https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=default_society&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news"+oid+"%2C"+aid+"&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page="+str(page)+"&refresh=false&sort=FAVORITE"  
# F12 > network > js > web_never_list_jsonp..... > copy link address > result > commentList > 0 , 1 , 2...

r=requests.get(c_url, headers=header) 

data = r.text
idx1 = data.find('(')   
idx2 = data.find(')')
#print(idx1)
#print(idx2)

json_data = data[idx1+1:idx2]
#print(json_data)
#print(type(json_data))
json_data = json.loads(json_data)
#print(type(json_data))

print(json_data['result']['commentList'][0]['maskedUserId'])
print(json_data['result']['commentList'][0]['contents'])
print(json_data['result']['commentList'][0]['regTime'][:10])
