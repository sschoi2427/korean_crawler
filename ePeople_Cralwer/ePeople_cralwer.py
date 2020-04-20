# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:52:58 2019

@author: sec

크롤링 소스
https://www.epeople.go.kr/jsp/user/pp/UPpProposOpenList.paid?flag=A&pageNo=1&mode=&petiNo=&s_date=20180212&e_date=20190211&ancCode=&sortType=&sortTemp=&snsTokenMessage=%255B%25EA%25B5%25AD%25EB%25AF%25BC%25EC%25A0%259C%25EC%2595%2588%255D%2B%25EA%25B3%25B5%25EA%25B0%259C%25EC%25A0%259C%25EC%2595%2588&reg_d_s=2018-02-12&reg_d_e=2019-02-11&divCode=&s_anc_c=6260000&status=&keyfield=petiTitle&keyword=
"""

import time

now = time.localtime()
tm_1 = "%04d.%02d.%02d" % (now.tm_year, now.tm_mon, now.tm_mday)

print("\n국민신문고 > 공개제안 > 상세검색:기관:부산광역시 크롤링을 시작합니다. ")
print("\n(신문고는 최대 1년까지만 출력할 수 있습니다.")
print("  해당 시간부터 1년까지의 기록을 출력하겠습니다.)")

e_date = input("출력할 날짜를 적으세요. 예시){} \n".format(tm_1))
page = int(input("출력할 페이지의 숫자를 적으세요. 예시) 1 \n"))
time.sleep(2) #2초간 대기


#날짜 변수 지정
e_date = e_date.replace(".",'')
s_date = str(int(e_date) - 9999)

#레지스트 날짜 변수 지정
s_date_r1 = s_date[:4]+"-"
s_date_r2 = s_date[4:6]+"-"
s_date_r3 = s_date[6:8]
e_date_r1 = e_date[:4]+"-"
e_date_r2 = e_date[4:6]+"-"
e_date_r3 = e_date[6:8]




#상대위치_폴더생성
import os
DATA_PATH = os.getcwd().replace('\\','/')
RESULT_PATH = DATA_PATH + "/result/"

dir_path = DATA_PATH
dir_name = 'result'
if not os.path.exists('./result/'):    
    os.mkdir(dir_path + '/' + dir_name + '/')

print("\n>>>> result 폴더가 생성되고, 결과가 저장됩니다. <<<<")
time.sleep(2) #2초간 대기

print("")
print("보안이 강한 post주소를 selenium으로 직접 접근하므로, 속도가 느릴 수 있습니다.\n")
print(">>>> ..로딩중입니다. 열린 인터넷 창을 끄거나 클릭하지 말고, 잠시만 기다려주세요. <<<<\n")




import requests as req
from bs4 import BeautifulSoup as bs
from selenium import webdriver

#내용을 임시 저장할 텍스트 파일 이름
txt_file_name = 'ePeople_content' 

#클리커 & 크롤러
def clicker_and_crawler(page):
    
    f = open(RESULT_PATH + txt_file_name +'.txt', 'w', encoding='utf-8')
    
    for page in range(1, page+1):
        
        # ★ 신문고_주소
        base_url = "https://www.epeople.go.kr/jsp/user/pp/UPpProposOpenList.paid?flag=A&pageNo="+str(page)+"&mode=&petiNo=&s_date=" + s_date + "&e_date=" + e_date + "&ancCode=&sortType=&sortTemp=&snsTokenMessage=%255B%25EA%25B5%25AD%25EB%25AF%25BC%25EC%25A0%259C%25EC%2595%2588%255D%2B%25EA%25B3%25B5%25EA%25B0%259C%25EC%25A0%259C%25EC%2595%2588&reg_d_s="+s_date_r1 + s_date_r2 + s_date_r3+"&reg_d_e="+e_date_r1 + e_date_r2 + e_date_r3+"&divCode=&s_anc_c=6260000&status=&keyfield=petiTitle&keyword="
        
        browser = webdriver.Chrome( os.getcwd().replace('\\','/')+"/chromedriver/chromedriver.exe" )
        browser.set_window_size(700, 700)
        browser.get( base_url ) #브라우저 열기

        source_code = req.get(base_url)
        plain_text = source_code.content
        soup = bs(plain_text, 'lxml')
        
        try:
            #페이지이동
            for num in soup.select('tr > td:nth-of-type(1)'):
                num = num.text
                browser.find_element_by_xpath('//*[@id="ancDetail_{}"]'.format(num)).click()
            
            #크롤링
                date = browser.find_element_by_xpath('//*[@id="content"]/div[3]/div[1]/table/tbody/tr[2]/td/ul/li[1]/p/span' or '//*[@id="content"]/div[3]/div/table/tbody/tr[2]/td/ul/li[1]/p/span').text
                f.write(date + "\t")
            
                head = browser.find_element_by_xpath('//*[@id="content"]/div[3]/div/table/thead/tr/th[2]').text
                f.write(head + "\t")
            
            
                one = browser.find_element_by_xpath('//*[@id="content"]/div[3]/div[1]/table/tbody/tr[1]/td/div/p[2]').text
                one = one.replace('\n',' ').replace('https://','').replace('http://','')
                f.write(one + "\t")
            
                two = browser.find_element_by_xpath('//*[@id="content"]/div[3]/div[1]/table/tbody/tr[1]/td/div/p[4]').text
                two = two.replace('\n',' ').replace('https://','').replace('http://','')
                f.write(two + "\t")
            
                three = browser.find_element_by_xpath('//*[@id="content"]/div[3]/div[1]/table/tbody/tr[1]/td/div/p[6]').text
                three = three.replace('\n',' ').replace('https://','').replace('http://','')
                f.write(three + "\n")
                
                print(num , "번 크롤링 완료")
                
                browser.execute_script("window.history.go(-1)")
                
            print("========== {}번째 페이지 크롤링 완료. 잠시만 기다려주세요. ==========".format(page))
            
        except Exception as e:
            print(num , "번 크롤링 실패, 에러 발생")
            print(e)
            continue
        
           
        browser.quit() #브라우저 종료
    f.close()
    
clicker_and_crawler(page)






import pandas as pd

#텍스트파일을 엑셀파일로 변경하여 저장
xl_file_name ='ePeople_result'

def excel_make():    
    data = pd.read_csv(RESULT_PATH + txt_file_name+'.txt', sep='\t',header=None, error_bad_lines=False)
    data.columns = ['date','title','problem','improvement','expect']
    print(data)    
    
    try:
        data.to_excel( RESULT_PATH + xl_file_name+'.xlsx', encoding='utf-8')
    except Exception as e:
        print(e)
    finally:
        print("\n▲▲▲▲▲▲▲▲▲▲▲▲ {}.xlsx파일로 저장이 완료되었습니다. ▲▲▲▲▲▲▲▲▲▲▲▲".format(xl_file_name))
        
excel_make()





