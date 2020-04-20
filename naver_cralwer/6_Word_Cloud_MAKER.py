# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 15:00:56 2019

@author: sec
"""

import os
DATA_PATH = os.getcwd().replace('\\','/')
RESULT_PATH = DATA_PATH + "/result/"

dir_path = DATA_PATH
dir_name = 'result'
if not os.path.exists('./result/'):    
    os.mkdir(dir_path + '/' + dir_name + '/')

print("\n>>>>>> result 폴더가 생성되고, 결과가 저장됩니다. <<<<<< \n")





from konlpy.tag import Hannanum
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

file_name = input("엑셀 파일 이름을 확장자 제외하고 넣으세요 \n")
number = int(input("상위 n개의 단어를 워드클라우드로 만듭니다. n을 넣으세요. ex)10 \n" ))
    
f = open(RESULT_PATH + file_name + '.txt', 'r', encoding="UTF-8") #다시 읽기
data = f.read()

try:
    engin = Hannanum()
    nouns = engin.nouns(data)

    nouns = [ n for n in nouns if len(n) > 1 ]
    count = Counter(nouns)
    tags = count.most_common(number)
    print(tags)

    wordcloud = WordCloud(font_path="C:/Windows/Fonts/malgun.ttf",
                      background_color='white', width=640, height=480)

    wordcloud.generate_from_frequencies(dict(tags))

    fig = plt.figure()
    plt.axis('off')
    plt.imshow(wordcloud)

except Exception as e:
    print(e)



