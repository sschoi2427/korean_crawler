# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 14:48:24 2019

@author: sec
"""

import time

now = time.localtime()
tm_1 = "%04d" % (now.tm_year)
tm_2 = "%04d.%02d.%02d" % (now.tm_year, now.tm_mon, now.tm_mday)
tm_3 = "(%04d-%02d-%02d %02dh_%02dm_%02ds)" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

query = input("네이버에서 크롤링 할 내용을 적으세요 예시)블록체인\n" )
s_date = input("크롤링 할 시작할 날짜를 적으세요. 예시){}.01.01 \n".format(tm_1))
e_date = input("크롤링 할 마지막 날짜를 적으세요. 예시){} \n".format(tm_2))
title_page = int(input("제목을 출력합니다. 페이지의 숫자를 적으세요. 예시) 1 \n"))


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

def crawler_title(line):
    print("{}페이지까지 출력됩니다.".format(line))   
    
    base_url = "https://search.naver.com/search.naver?&where=news&query=" + query + "&sm=tab_pge&sort=0&photo=0&field=0&reporter_article=&pd=1&ds=" + s_date + "&de=" + e_date + "&docid=&nso=so:r,p:1w,a:all&mynews=0&cluster_rank=29&start="
    
    f = open(RESULT_PATH + "title_result {}.txt".format(tm_3), 'w', encoding="UTF-8")
    
    for i in range(0, line) :
        print("==============={}페이지입니다.===============".format(i+1))
        
        i = (i*10)+1
        url = base_url + "{}".format(i)
        source_code = req.get(url)
        plain_text = source_code.text
        soup = bs(plain_text, 'lxml')
        
        for title in soup.select('ul > li > dl > dt > a'):
            title = title.text
            print(title)
            f.write(title + "\n")
        f.write("\n")
    f.close
    
    print(soup.select('ul > li > dl > dt > a'))
    
print("===========================================")     
crawler_title(title_page)


print("▲▲▲▲▲ 입력한 페이지의 모든 기사 제목을 텍스트파일로 저장했습니다. ▲▲▲▲▲")
   

