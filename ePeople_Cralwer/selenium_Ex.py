# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 10:29:40 2019

@author: sec
"""

from selenium import webdriver
import time

browser = webdriver.Chrome("C:/Users/sec/Desktop/chromedriver/chromedriver.exe")
browser.set_window_size(1024, 680)

page = 1

url = "https://www.epeople.go.kr/jsp/user/pp/UPpProposOpenList.paid?flag=A&pageNo="+str(page)+"&mode=&petiNo=&s_date=20180201&e_date=20190131&ancCode=&sortType=&sortTemp=&snsTokenMessage=%255B%25EA%25B5%25AD%25EB%25AF%25BC%25EC%25A0%259C%25EC%2595%2588%255D%2B%25EA%25B3%25B5%25EA%25B0%259C%25EC%25A0%259C%25EC%2595%2588&reg_d_s=2018-02-01&reg_d_e=2019-01-31&divCode=&s_anc_c=6260000&status=&keyfield=petiTitle&keyword="
browser.get( url )

# one = browser.find_element_by_xpath('//*[@id="ancDetail_{0}"]'.format(i)).click()
# browser.execute_script("window.history.go(-1)") #뒤로가기
    
time.sleep(5) #1초대기
browser.quit() #브라우저 종료