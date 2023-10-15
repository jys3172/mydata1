from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import pymysql
from sqlalchemy import create_engine

# MySQL Connector using pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import time
# # import csv
# import pymysql
# con = pymysql.connect(host='localhost',
#                         user='root',
#                         password='1234',
#                         db='nair',
#                         charset='utf8')

# mycursor = con.cursor()

# query = """
# select + from nair;
# """

# mycursor.execute(query)
# data = mycursor.fetchall()
# con.close()


#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#브라우저 사람행동
chrome_options.add_argument("--disable-blink-features=AutomationControlled")

#불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=chrome_options)

#웹페이지 해당 주소 이동
driver.get("http://flight.naver.com/")
time.sleep(3)

#도착지 클릭
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[1]/button[2]').click()
time.sleep(1)
#//*[@id="__next"]/div/div/div[11]/div[1]/div/input
#//*[@id="__next"]/div/div/div[11]/div[1]/div
#//*[@id="__next"]/div/div/div[11]/div[1]

#도착지 입력
where = input('어디로 가실건가요?')
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[10]/div[1]/div/input').send_keys(where)
time.sleep(1)
driver.find_element(By.CLASS_NAME, 'autocomplete_airport__3zusQ').click()

#출발일 클릭
driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[2]/button[1]').click()
time.sleep(1)


#가는 날짜 입력
print("가는 날짜 입력")

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

#가는날 선택
driver.find_elements(By.XPATH, f'//b[text() = "{dayInput}"]')[monthInput].click()
time.sleep(1)


#오는 날짜 입력
print("오는 날짜 입력")

 # 월 선택
months2 = ['이번 달', '다음 달']
for i, months in enumerate(months2):
    print(f'{i + 1}. {months}\t', end='\t')
print()
monthInputs = int(input("몇월에 떠나시나요? : "))-1
print()

# 요일 선택
dayInput = int(input("몇일에 떠나시나요? : "))
print()

#오는날 선택
driver.find_elements(By.XPATH, f'//b[text() = "{dayInput}"]')[monthInputs].click()
#driver.find_elements(By.XPATH, '//b[text() = "24"]')[0].click()
time.sleep(1)


# 달력 선택의 Xpath를 분석한 결과 /div[Month]/table/tbody/tr[Week]/td[Day] 임을 알 수 있습니다.

driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/button')[0].click()
time.sleep(5)

# # 파일 생성
# f = open(r"C:\Users\조영상\Desktop\pythonwork\selenium\dataa.csv", 'w', encoding = 'CP949', newline='')
# csvWriter = csv.writer(f)
# time.sleep(1)


# concurrent_ConcurrentItemContainer__2lQVG result
# 항공사: airline
# 출발 route_Route__2UInh[0]
# 도착 route_Route__2UInh[1]
# 가격 item_firstItem__15zkv

airline_list =[]
startTime_list =[]
returnTime_list =[]
price_list =[]

results = driver.find_elements(By.CLASS_NAME,'concurrent_ConcurrentItemContainer__2lQVG.result')
for result in results:
    try:
        airline = result.find_element(By.CLASS_NAME, 'airline').text
        startTime = result.find_elements(By.CLASS_NAME, 'route_Route__2UInh')[0].text
        returnTime = result.find_elements(By.CLASS_NAME, 'route_Route__2UInh')[1].text
        price = result.find_element(By.CLASS_NAME, 'item_firstItem__15zkv').text
        
        print(airline, startTime, returnTime, price)

        airline_list.append(airline)
        startTime_list.append(startTime)
        returnTime_list.append(returnTime)
        price_list.append(price)
        
        # print(f'항공사 : {airline}')
        # print(f'출발 : {startTime}')
        # print(f'귀국 : {returnTime}')
        # print(f'가격 : {price}')
        # print('-'*100)
    except:
        pass
time.sleep(8)

print("항공권: ",len(airline_list))
print("출발: ",len(startTime_list))
print("귀국: ",len(returnTime_list))
print("가격: ",len(price_list))

df = pd.DataFrame({'항공명': airline_list, '출발':startTime_list, '귀국':returnTime_list, '가격': price_list})
print(df)

db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='AIR', charset='utf8')
cursor = db.cursor()

#cursor = db.cursor()

sql = "DROP TABLE IF EXISTS airline"

cursor.execute(sql)

sql = '''
CREATE TABLE airline (
    airline VARCHAR(10) NOT NULL PRIMARY KEY,
    startTime VARCHAR(10) NOT NULL,
    returnTime VARCHAR(10) NOT NULL,
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
df.to_sql(name='airline', con=engine, index=False, if_exists='replace')
conn.close()

input()
