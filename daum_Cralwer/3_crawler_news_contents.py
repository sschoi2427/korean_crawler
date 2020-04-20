# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 13:09:15 2019

@author: sec
"""

import time

now = time.localtime()
tm_1 = "%04d" % (now.tm_year)
tm_2 = "%04d.%02d.%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
tm_3 = "(%04d-%02d-%02d %02dh_%02dm_%02ds)" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

query = input("다음에서 크롤링 할 내용을 적으세요 예시)블록체인\n").replace(" ","+")
s_date = input("크롤링 할 시작할 날짜를 적으세요. 예시){}.01.01 \n".format(tm_1))
e_date = input("크롤링 할 마지막 날짜를 적으세요. 예시){} \n".format(tm_2))
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

def crawler_contents(page):
    
    print("{}페이지까지 출력됩니다.".format(page))
    
    f = open(RESULT_PATH + '/contents.txt', 'w', encoding='utf-8')
    
    for i in range(0, page):
        print("==============={}페이지가 출력되었습니다..===============".format(i+1))
        base_url = "https://search.daum.net/search?DA=STC&cluster=y&cluster_page=0&ed="+e_date.replace(".",'')+"235959&enc=utf8&https_on=on&p="+str(page)+"&period=u&q="+query+"&sd="+s_date.replace(".",'')+"000000&w=news"
        i += 1
                                                                  # header = {
                                                                        # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                                                                        # }  
        News_req = req.get(base_url)                                    # headers=header가 필요하면 인수 삽입 / #print(base_url)      
        contents = News_req.content #html값만 추출
        soup = bs(contents, 'lxml')                                     # print(soup) 필요하다면 사용
                                                                       # select는 css접근하는 형식으로 작성을 해주면되고, find_all함수는 아래와 같이 {}안에 값을 넣어서 처리
        for urls in soup.select("div > span > .f_nb"):                 # 검색 쿼리 F12 : dt > dd > <a class=._sp_each_url>
            try :                                                       # print(urls["href"])
                news_detail = get_news(urls.get('href'))
                f.write("{}\t{}\t{}\t{}\n".format(news_detail[1], news_detail[3], news_detail[0], news_detail[2]))
            except Exception as e:
                print(e)
                continue

    f.close()


def get_news(urls):
    
    news_detail = []
    
    news_req = req.get(urls)
    news_soup = bs(news_req.content, 'lxml')
    print(urls)
    
    page_title = news_soup.select('.tit_view')[0].text                                  
    news_detail.append(page_title)
    
    page_date = news_soup.select('.info_view')[0].get_text()
    page_date = page_date.split("입력 ")[1]
    page_date = page_date[:10]
    news_detail.append(page_date)
    
    page_text = news_soup.select('div.news_view')[0].get_text().replace('\n', " ") #<div id=articleBodyContents.../>
    news_detail.append(page_text)                                                                  #news_detail.append(s_text.strip())

    page_company = news_soup.select('strong.tit_cp')[0].get_text() #footer > id address > a
    page_company = page_company.split(" 주요")[:1]
    news_detail.append(page_company)
    
    return news_detail                                                  #new_detail이 가진 index[0, 1, 2, 3]과 [내용] 반환
    #print(news_detail)

    
crawler_contents(page)





import pandas as pd

def excel_make():
    data = pd.read_csv(RESULT_PATH+'/contents.txt', sep='\t',header=None, error_bad_lines=False)
    data.columns = ['years','company','title','contents']
    print(data)
    xlsx_name = RESULT_PATH + '/contents_result {}'.format(tm_3) + '.xlsx'
    data.to_excel(xlsx_name, encoding='utf-8')

excel_make()



print("▲▲▲▲▲▲▲▲▲▲▲▲ 검색내용 > '네이버뉴스'의 내용을 엑셀파일에 저장합니다.▲▲▲▲▲▲▲▲▲▲▲▲")

