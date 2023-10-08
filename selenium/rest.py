import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

import pandas as pd
import numpy as np
import time                      # 파이썬 너무 빨라서 꼬이는 것 방지.

from bs4 import BeautifulSoup    # html 데이터를 전처리
from selenium import webdriver   # 웹 브라우저 자동화
from tqdm import tqdm_notebook   # for문 돌릴 때 진행상황을 %게이지로
from selenium.webdriver.common.keys import Keys  # 엔터키 누르기

#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

#브라우저 꺼짐 방지
path = Options()
path.add_experimental_option("detach", True)

#불필요한 에러 메세지 없애기
path.add_experimental_option("excludeSwitches",["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options = path)     

# 네이버 호텔 사이트 접속
driver.get('https://hotel.naver.com/hotels/main')    
time.sleep(2) 

#목적지 클릭
element = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div/div/div[1]/button').click()
time.sleep(1)

#도착지 입력
where = input('어디로 가실건가요?')
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div/input').send_keys(where)
time.sleep(1)

driver.find_element(By.CLASS_NAME, 'SearchResults_anchor__luLYP').click()
driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div/div/div[2]/button[1]').click()
time.sleep(1)

#가는 날 선택
 # 월 선택
months = ['이번 달', '다음 달']
for i, month in enumerate(months):
    print(f'{i + 1}. {month}\t', end='\t')
print()
monthInput = int(input("몇월에 떠나시나요? : "))-1
print()

# 요일 선택
dayInput = int(input("몇일에 떠나시나요? : "))
print()

driver.find_elements(By.XPATH, f'//b[text() = "{dayInput}"]')[monthInput].click()

# 돌아오는 날 선택
 # 월 선택
months = ['이번 달', '다음 달']
for i, month in enumerate(months):
    print(f'{i + 1}. {month}\t', end='\t')
print()
monthInput = int(input("몇월에 돌아오시나요? : "))-1
print()

# 요일 선택
dayInput = int(input("몇일에 떠나시나요? : "))
print()

driver.find_elements(By.XPATH, f'//b[text() = "{dayInput}"]')[monthInput].click()
time.sleep(2)


#적용 버튼 클릭
driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[2]/div[4]/button').click()
driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div/button').click()
time.sleep(10)


#정보 가져오기
results = driver.find_elements(By.CLASS_NAME,'SearchList_HotelItem__aj2GM')
for result in results:
    try:
        title = result.find_element(By.CLASS_NAME, 'Detail_title__40_dz').text
        location = result.find_element(By.CLASS_NAME, 'Detail_location__u3_N6').text
        rating = result.find_element(By.CLASS_NAME, 'Detail_score__UxnqZ').text
        price = result.find_element(By.CLASS_NAME, 'Price_show_price__iQpms').text.replace('\n', ' ')
        print(f'숙소명 : {title}')
        print(f'지역 : {location}')
        print(f'별점 : {rating}')
        print(f'가격 : {price}')
        print('-'*100)
    except:
        pass

input()
