# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 15:36:15 2019

@author: sec
"""
#tm_1 = "%04d" % (now.tm_year)
#tm_2 = "%04d.%02d.%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
#query = input("네이버에서 크롤링 할 내용을 적으세요 예시)블록체인\n").replace(" ","+")
#s_date = input("크롤링 할 시작할 날짜를 적으세요. 예시){}.01.01 \n".format(tm_1))
#e_date = input("크롤링 할 마지막 날짜를 적으세요. 예시){} \n".format(tm_2))

import time
now = time.localtime()
tm_0 = "(%04d-%02d-%02d %02dh_%02dm_%02ds)" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

print("="*50+"\n먼저, '네이버 홈페이지'에 '검색 내용'을 입력하세요."); print("반드시 '뉴스' 파트의 '검색옵션'에서 설정을 하고 실행해주세요. \n"+"="*50)
query = input("네이버뉴스 '댓글'을 크롤링 합니다. 2페이지의 url를 입력해주세요. \n").split("start=")[0] + "start="
page = int(input("내용을 출력합니다. 페이지의 숫자를 적으세요. 예시) 1 \n"))
c_p_num_0 = int(input("각 기사에서 크롤링 할 댓글의 개수를 20단위로 적으세요. ex)20 40 60 \n"))
c_p_num = c_p_num_0//20

import os
DATA_PATH = os.getcwd().replace('\\','/')
RESULT_PATH = DATA_PATH + "/result/"

dir_path = DATA_PATH
dir_name = 'result'
if not os.path.exists('./result/'):    
    os.mkdir(dir_path + '/' + dir_name + '/')
    
print("\n>>>>>> result 폴더가 생성되고, '최신순'으로 결과가 저장됩니다. <<<<<< \n")




import re
import requests as req
from bs4 import BeautifulSoup as bs
import json

extra = "m_view=1&includeAllCount=true&"

view = "society" # view관련 오류시 F12 > network > js >json에서 확인후 it 등으로 이를 변경해주세요.

def crawler_comment(line):
    
    print("{0}페이지까지 댓글이 {1}개씩 출력됩니다.".format(line, c_p_num_0))
    
    print("==========================================")
    
    f = open(RESULT_PATH + 'comment.txt', 'w', encoding='UTF-8')
    
    base_url = query
     
    for i in range(0, line) :            
        i = (i*10)+1
        url = base_url + "{}".format(i)
        source_code = req.get(url)
        plain_text = source_code.text
        soup = bs(plain_text, 'lxml')
        
        for link in soup.select("dd > ._sp_each_url"):
            url = link.get('href')
            #print(url)
            url = url[:37] + extra + url[37:]
            print(url)
            
            oid = url.split("oid=")[1].split("&")[0] 
            aid = url.split("aid=")[1]
            
            header = { 
                    "User-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", 
                    "referer":url, 
                  }
            sort = "new" #FAVORITE            
            #c_p_num = 3
            for page_num in range(1, c_p_num+1):
                c_url="https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=view_"+ view +"&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news" + oid + "%2C" + aid + "&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=" + str(page_num) + "&refresh=false&sort="+sort
            #page = 1
            #c_url="https://apis.naver.com/commentBox/cbox/web_neo_list_jsonp.json?ticket=news&templateId=view_"+ view +"&pool=cbox5&_callback=jQuery1707138182064460843_1523512042464&lang=ko&country=&objectId=news" + oid + "%2C" + aid + "&categoryId=&pageSize=20&indexSize=10&groupId=&listType=OBJECT&pageType=more&page=" + str(page_num) + "&refresh=false&sort="+sort
            
                r=req.get(c_url, headers=header) 
            #print(r)
                data = r.text
            #print(data)
            
                idx1 = data.find('(')   
                idx2 = data.find(')')
            #print(idx1, idx2)
            
                try :
                    json_data = data[idx1+1:idx2]
                #print(type(json_data))
            
                    json_data = json.loads(json_data)
                #print(type(json_data))
            
                    if json_data['result']['commentList'] == []:
                        pass #댓글이 없습니다.
                    else : 
                        for j in range(0, len(json_data['result']['commentList'])):
                        #닉네임
                            name = json_data['result']['commentList'][j]['maskedUserId']
                       
                        #본문
                            content = json_data['result']['commentList'][j]['contents'].replace("\n", " ")
                            #이모티콘 제거
                            RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
                            contents = RE_EMOJI.sub(r'', content)
                       
                        #시간
                            time = json_data['result']['commentList'][j]['regTime'][:10]
                        
                            print(time, name, content)
                        
                            f.write("{}\t{}\t{}\t{}\n".format(time, url, name, contents))
                        print("==========================================")
                except Exception as e:
                    print(e)
                    print("예외가 발생하여 댓글을 제외하였습니다")
                    print("==========================================")
                    continue
    f.close()

        
crawler_comment(page)





import pandas as pd

def excel_make():
    data = pd.read_csv(RESULT_PATH + 'comment.txt', sep='\t',header=None)
    data.columns = ['time','url','name','contents']
    print(data)
    #url의 값이 2번째와 1번째가 동일하다면, 2번째는 ""로 표현하고 싶다
    xlsx_name = RESULT_PATH + 'comment_result {}'.format(tm_0) + '.xlsx'
    data.to_excel(xlsx_name, encoding='utf-8')
excel_make()

