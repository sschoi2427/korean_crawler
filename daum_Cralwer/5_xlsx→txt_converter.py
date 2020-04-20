# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:54:43 2019

@author: sec
"""

import os

DATA_PATH = os.getcwd().replace('\\','/')
RESULT_PATH = DATA_PATH + "/result/"

dir_path = DATA_PATH
dir_name = 'result'
if not os.path.exists('./result/'):    
    os.mkdir(dir_path + '/' + dir_name + '/')
    
print("\n>>>>>> result 폴더가 생성되고, 결과가 저장됩니다. <<<<<<")




import xlrd 

file_name = input("엑셀 파일의 이름을 확장자 제외하고 넣으세요 \n")
input_file_name = RESULT_PATH + file_name + ".xlsx"
    
wb = xlrd.open_workbook(input_file_name)
ws = wb.sheet_by_index(0)
ncol = ws.ncols
nlow = ws.nrows

f = open(RESULT_PATH + file_name + '.txt', 'w', encoding="UTF-8") #UTF-8로 저장

for i in range(1, nlow):
    contents = ws.col_values(4)[i]
    #contents.encode("UTF-8")
    f.write(contents)
    
f.close

print(str(int(nlow-1))+"개의 contents가 텍스트로 변환되었습니다.")



