# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 11:10:39 2019

@author: sec
"""


print("="*65)
print("트위터 크롤링을 시작합니다. ")
print("24시간 이전의 트윗만 크롤링 가능합니다. ")
print("="*65)

query = input("검색할 내용을 적으세요. 예시)빅데이터 \n")
query = query.replace(' ','%20')




import time 
import datetime as dt
now = time.localtime()
tm_1 = "%04d.%02d" % (now.tm_year, now.tm_mon)

startdate=input("검색 시작 날짜 입력 예시){}.01 \n".format(tm_1)).replace('.','-')
enddate=input("검색 끝 날짜 입력 \n").replace('.','-')

startdate_lsit = startdate.split('-')
start_dd = startdate_lsit.pop()
start_mm = startdate_lsit.pop()
start_yyyy = startdate_lsit.pop()
    
enddate_list = enddate.split('-')
end_dd = enddate_list.pop()
end_mm = enddate_list.pop()
end_yyyy = enddate_list.pop()
    
startdate = dt.date(year=int(start_yyyy),month=int(start_mm),day=int(start_dd)) #시작날짜 
untildate = dt.date(year=int(start_yyyy),month=int(start_mm),day=int(start_dd)+1) # 시작날짜 +1 
enddate = dt.date(year=int(end_yyyy),month=int(end_mm),day=int(end_dd)+1) # 끝날짜


order = input("정렬방식을 선택해주세요. ex) 1:인기순 2:최신순 \n")




import os
DATA_PATH = os.getcwd().replace('\\','/')
RESULT_PATH = DATA_PATH + "/result/"

dir_path = DATA_PATH
dir_name = 'result'
if not os.path.exists('./result/'):    
    os.mkdir(dir_path + '/' + dir_name + '/')
print('')
print("="*65)
print(">>>> result 폴더가 생성되고, 결과가 저장됩니다. <<<<\n")
print("..로딩중입니다. 열린 인터넷 창을 끄거나 클릭하지 말고, 잠시만 기다려주세요.")
print("="*65)
print('')
time.sleep(2) #2초간 대기






#import requests as req
from bs4 import BeautifulSoup as bs
from selenium import webdriver 

browser = webdriver.Chrome( os.getcwd().replace('\\','/')+"/chromedriver/chromedriver.exe" )

totaltweets=[] 
totaldate=[]
while not enddate==startdate:
    #인기순
    if order == "1": 
        base_url = 'https://twitter.com/search?q='+query+'%20since%3A'+str(startdate)+'%20until%3A'+str(untildate)+'&amp;amp;amp;amp;amp;amp;lang=eg' 
    #최신순
    elif order == "2": 
        base_url = 'https://twitter.com/search?f=tweets&q='+query+'%20since%3A'+str(startdate)+'%20until%3A'+str(untildate)+'&amp;amp;amp;amp;amp;amp;lang=eg' 
    else:
        browser.quit() #브라우저 종료
        print("★★★ 에러 : 정렬방식을 '인기순', '최신순' 중 하나만 입력해주세요.★★★")
        break
            
    #base_url='https://twitter.com/search?q='+query+'%20since%3A'+str(startdate)+'%20until%3A'+str(untildate)+'&amp;amp;amp;amp;amp;amp;lang=eg' 
    
    
    browser.set_window_size(700, 700)
    browser.get(base_url)
    
    html = browser.page_source 
    soup=bs(html,'lxml') 
     
    lastHeight = browser.execute_script("return document.body.scrollHeight")  #스크롤의 높이를 리턴
    
    try:
        while True:      
            dailyfreq={'Date' : startdate} 
            wordfreq=0 
            tweets1=soup.find_all("p", {"class": "TweetTextSize"})
            tweets2=soup.find_all("span", {"class": "_timestamp js-short-timestamp "})
        
            #스크롤 down
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") #스크롤을 내려 맨 밑의 높이를 0으로 만든다.
            time.sleep(1) 
            newHeight = browser.execute_script("return document.body.scrollHeight") # 새로 생성된 스크롤의 높이를 리턴
        
            #스크롤 down : if 내린것 ≠ 원래것
            if newHeight != lastHeight: 
                html = browser.page_source 
                soup=bs(html,'lxml')
                tweets1=soup.find_all("p", {"class": "TweetTextSize"})
                tweets2=soup.find_all("span", {"class": "_timestamp js-short-timestamp "})
            
        #스크롤 down : else 내린것 = 원래것 : 처음으로가서 날짜가 더해진다.
            else: 
                dailyfreq['Frequency'] = wordfreq
                wordfreq = 0
                startdate = untildate               #다시 맨 위로
                untildate += dt.timedelta(days=1)   #1씩 더해서 나타난다 timedelta:시간의 연산
                dailyfreq = {}
                totaltweets.append(tweets1)
                totaldate.append(tweets2)
                break 

            lastHeight = newHeight
            
            
    except Exception as e:
            print("크롤링 실패, 에러 발생")
            print(e)
            continue    
       
        

        
        
        
        
import pandas as pd     

df = pd.DataFrame(columns=['yyyymmdd','message'])

    
for i in range(len(totaltweets)):
    for j in range(len(totaltweets[i])):
        messages = (totaltweets[i][j]).text
        messages = messages.replace('\n',' ').replace('http://','').replace('https://','')
        yymmdd = (totaldate[i][j]).text
        df = df.append({'yyyymmdd': yymmdd, 'message': messages}, ignore_index=True)

xl_file_name ='twitter_result'

df.to_excel(RESULT_PATH + xl_file_name +".xlsx",sheet_name='sheet1')        
print(df)



