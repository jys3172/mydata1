import sys
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import pandas as pd
import numpy as np
import pymysql
from sqlalchemy import create_engine
import requests

random_se = random.uniform(1,2)
random_sec = random.uniform(7,10)

# MySQL Connector using pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
from bs4 import BeautifulSoup    # html 데이터를 전처리
from tqdm import tqdm_notebook   # for문 돌릴 때 진행상황을 %게이지로

#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager


#브라우저 꺼짐 방지
path = Options()
path.add_experimental_option("detach", True)
path.add_argument("--disable-blink-features=AutomationControlled")

#불필요한 에러 메세지 없애기
path.add_experimental_option("excludeSwitches",["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options = path)     

# 네이버 호텔 사이트 접속
driver.get('https://hotel.naver.com/hotels/main')    
time.sleep(2) 
html = requests.get('https://hotel.naver.com/hotels/main').text

#목적지 클릭
element = driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div/div/div[1]/button').click()
time.sleep(random_se)

#도착지 입력
where = input('어디로 가실건가요?')
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div[2]/div[1]/div/input').send_keys(where)
time.sleep(random_se)

driver.find_element(By.CLASS_NAME, 'SearchResults_anchor__luLYP').click()
driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div/div/div[2]/button[1]').click()
time.sleep(random_se)

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
time.sleep(1)

# 돌아오는 날 선택
 # 월 선택
months = ['이번 달', '다음 달']
for i, month in enumerate(months):
    print(f'{i + 1}. {month}\t', end='\t')
print()
monthInput = int(input("몇월에 돌아오시나요? : "))-1
print()

# 요일 선택
dayInput = int(input("몇일에 돌아오시나요? : "))
print()

driver.find_elements(By.XPATH, f'//b[text() = "{dayInput}"]')[monthInput].click()
time.sleep(random_se)


#적용 버튼 클릭
driver.find_element(By.XPATH,'//*[@id="__next"]/div/div[2]/div[4]/button').click()
time.sleep(1)
driver.find_element(By.XPATH,'//*[@id="__next"]/div/div/div[2]/div/div/button').click()
time.sleep(5)

# 정보 저장 리스트
title_list =[]
location_list =[]
rating_list =[]
price_list =[]

#정보 가져오기
results = driver.find_elements(By.CLASS_NAME,'SearchList_HotelItem__aj2GM')
for result in results:
    try:
        title = result.find_element(By.CLASS_NAME, 'Detail_title__40_dz').text
        location = result.find_element(By.CLASS_NAME, 'Detail_location__u3_N6').text
        rating = result.find_element(By.CLASS_NAME, 'Detail_score__UxnqZ').text
# Detail_score__UxnqZ
# //*[@id="__next"]/div/div/div/div[1]/div[3]/ul/li[1]/div[1]/div[2]/div/i[1]/text()
# //*[@id="__next"]/div/div/div/div[1]/div[3]/ul/li[1]/div[1]/div[2]/div/i[1]
        price = result.find_element(By.CLASS_NAME, 'Price_show_price__iQpms').text
# //*[@id="__next"]/div/div/div/div[1]/div[3]/ul/li[1]/div[2]/em
# Price_show_price__iQpms
#__next > div > div > div > div.Contents_ListCompon
#ent__39yRH > div.Contents_result___1Z0_ > ul > li:nth-child(1) > div.Price_Price__7vul8 > em
        print(title, location, rating, price)

        title_list.append(title)
        location_list.append(location)
        rating_list.append(rating)
        price_list.append(price)

        # print(f'숙소명 : {title}')
        # print(f'지역 : {location}')
        # print(f'별점 : {rating}')
        # print(f'가격 : {price}')
        # print('-'*100)
    except:
        pass
time.sleep(random_sec)

print("이름: ",len(title_list))
print("장소: ",len(location_list))
print("별점: ",len(rating_list))
print("가격: ",len(price_list))

df = pd.DataFrame({'이름': title_list, '장소': location_list, '별점': rating_list, '가격': price_list})
print(df)

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='AIR', charset='utf8')
cursor = db.cursor()


sql = "DROP TABLE IF EXISTS rest"
cursor.execute(sql)

sql = '''
CREATE TABLE rest (
    title VARCHAR(10) NOT NULL PRIMARY KEY,
    location VARCHAR(10) NOT NULL,
    rating VARCHAR(10) NOT NULL,
    price  VARCHAR(10) NOT NULL
);
'''
cursor.execute(sql)
db.commit()
db.close()

engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
.format(user="root",
pw="1234",
db="air"))

conn = engine.connect()

# dataframe -> mysql DB table
df.to_sql(name='rest', con=engine, index=False, if_exists='replace')
conn.close()

input()


