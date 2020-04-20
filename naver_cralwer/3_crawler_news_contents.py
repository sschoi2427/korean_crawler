# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 13:09:15 2019

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
print("="*50+"\n먼저, '네이버 홈페이지'에 '검색내용'을 입력하세요."); print("반드시 '뉴스' 파트의 '검색옵션'에서 설정을 하고 실행해주세요. \n"+"="*50)
query = input("네이버뉴스를 크롤링 합니다. 2페이지의 url를 입력해주세요. \n").split("start=")[0] + "start="
page = int(input("내용을 출력합니다. 페이지의 숫자를 적으세요. 예시) 1 \n"))



import os

DATA_PATH = os.getcwd().replace('\\','/')
RESULT_PATH = DATA_PATH + "/result/"

dir_path = DATA_PATH
dir_name = 'result'
if not os.path.exists('./result/'):    
    os.mkdir(dir_path + '/' + dir_name + '/')
    
print("\n>>>>>> result 폴더가 생성되고, 결과가 저장됩니다. <<<<<< \n")



import requests as req
from bs4 import BeautifulSoup as bs

def crawler_contents(line):
    
    print("{}페이지까지 출력됩니다.".format(line))
    
    f = open(RESULT_PATH + '/contents.txt', 'w', encoding='utf-8')
    
    for i in range(0, line):
        print("==============={}페이지가 출력되었습니다..===============".format(i+1))
        
        base_url = query
        
        i = (i*10)+1                                                      # header = {
        base_url = base_url + "{}".format(i)                            # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                                                                        # }  
        News_req = req.get(base_url)                                    # headers=header가 필요하면 인수 삽입 / #print(base_url)      
        contents = News_req.content #html값만 추출
        soup = bs(contents, 'lxml')                                     # print(soup) 필요하다면 사용
                                                                        # select는 css접근하는 형식으로 작성을 해주면되고, find_all함수는 아래와 같이 {}안에 값을 넣어서 처리
        for urls in soup.select("dd > ._sp_each_url"):                 # 검색 쿼리 F12 : dt > dd > <a class=._sp_each_url>
            try :                                                       # print(urls["href"])
                if urls["href"].startswith("https://news.naver.com"):   # startswith()함수 인수안의 문자가 발견되면 true, 그렇지 않으면 false 반환
                                                                        # print(urls["href"])
                    news_detail = get_news(urls["href"])
                    # news_detail = [date=1, company=3, title=0, text=2]
                    f.write("{}\t{}\t{}\t{}\n".format(news_detail[1], news_detail[3], news_detail[0], news_detail[2])) # \t로 각 문자 리스트를 구분하여 문자열로 변환
                    #print( news_detail )           
            except Exception as e:
                print(e)
                continue

    f.close()

                    

def get_news(urls):
    
    news_detail = []                                                    # 리스트생성 및 초기화
    
    news_req = req.get(urls)                                            # url가져오기
    news_soup = bs(news_req.content, 'lxml')                            #html.parserd에서 성능 upgrade
    print(urls)

    page_title = news_soup.select('h3#articleTitle')[0].text.replace('\n\n'," ").replace('\n', " ")            # 소스 : <h3 id=articleTitle..../>
    news_detail.append(page_title)

    page_date = news_soup.select('.t11')[0].get_text()[:11]             #div > span > <sponsor class=t11.../> 10자리까지의 문자열만
    news_detail.append(page_date)

    page_text = news_soup.select('#articleBodyContents')[0].get_text().replace('\n\n\n'," ").replace('\n\n'," ").replace('\n', " ").replace('\t\t', " ").replace('\t'," ") #<div id=articleBodyContents.../> #javaScript부분의 주석이 출력 되므로, " "로 변경
    s_text = page_text.replace("// flash 오류를 우회하기 위한 함수 추가 function _flash_removeCallback() {}", "")
    #for j in range(50, 1, -1):
    #    s_text = s_text.replace('\n'*j," ").format(j)
    news_detail.append(s_text.strip())
                                                                        #news_detail.append(s_text.strip())
    page_company = news_soup.select('#footer address')[0].a.get_text()  #footer > id address > a
    news_detail.append(page_company)
    
    
    return news_detail                                                  #new_detail이 가진 index[0, 1, 2, 3]과 [내용] 반환
    
crawler_contents(page)




import pandas as pd

def excel_make():
    data = pd.read_csv(RESULT_PATH + 'contents.txt', sep='\t',header=None, error_bad_lines=False, warn_bad_lines=False, encoding='utf8', engine='python')
    data.columns = ['years','company','title','contents']
    print(data)
    xlsx_name = RESULT_PATH + 'contents_result {}'.format(tm_0) + '.xlsx'
    data.to_excel(xlsx_name, encoding='utf-8')

excel_make()



print("▲▲▲▲▲▲▲▲▲▲▲▲ 검색내용 > '네이버뉴스'의 내용을 엑셀파일에 저장합니다.▲▲▲▲▲▲▲▲▲▲▲▲")

