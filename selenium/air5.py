from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import pymysql
from sqlalchemy import create_engine
import asyncio
from flask import Flask, jsonify # render_template, request
import timer

# MySQL Connector using pymysql
pymysql.install_as_MySQLdb()
import MySQLdb
import time

#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])


# async def crawl_data():
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

# 각 데이터 리스트에 저장
airline_list =[]
startTime_list =[]
returnTime_list =[]
price_list =[]

# 데이터 최대 30개로 제한
max_data_count = 30
current_data_count = 0

results = driver.find_elements(By.CLASS_NAME,'concurrent_ConcurrentItemContainer__2lQVG.result')
for result in results:
    try:
        airline = result.find_element(By.CLASS_NAME, 'airline').text
        startTime = result.find_elements(By.CLASS_NAME, 'route_Route__2UInh')[0].text
        returnTime = result.find_elements(By.CLASS_NAME, 'route_Route__2UInh')[1].text
        price = result.find_element(By.CLASS_NAME, 'item_firstItem__15zkv').text
        
        print(airline, startTime, returnTime, price)

        if current_data_count < max_data_count:
            airline_list.append(airline)
            startTime_list.append(startTime)
            returnTime_list.append(returnTime)
            price_list.append(price)
            current_data_count +=1
        else:
            break
        
    except:
        pass
time.sleep(15)

print("항공권: ",len(airline_list))
print("출발: ",len(startTime_list))
print("귀국: ",len(returnTime_list))
print("가격: ",len(price_list))


df = pd.DataFrame({'항공명': airline_list, '출발':startTime_list, '귀국':returnTime_list, '가격': price_list})
print(df)
# driver.quit()

# async def main():
#     await crawl_data()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

# 데이터베이스 호출
db = pymysql.connect(host='localhost', port=3306, user='root', passwd='1234', db='AIR', charset='utf8')
cursor = db.cursor()

# 테이블 존재할 시 제거후 시작
sql = "DROP TABLE IF EXISTS airline"

cursor.execute(sql)

# 테이블 생성
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
# driver.quit()
time.sleep(1)


# async def main():
#     await crawl_data()

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())

sensor_db = pymysql.connect(
    user='root', 
    passwd='1234', 
    host='127.0.0.1', 
    db='air', 
    charset='utf8'
)

#cursor = sensor_db.cursor(pymysql.cursors.DictCursor)
cursor = sensor_db.cursor()

#sql = "DELETE FROM sensor WHERE _id = 2;"
sql = "SELECT * FROM airline"

cursor.execute(sql)
data_list = cursor.fetchall()

# sensor_db.commit()
# sensor_db.close()


#Flask 객체 인스턴스 생성
app = Flask(__name__)

@app.route('/', methods=['GET']) # 접속하는 url
def index():
    
    sql = "SELECT 항공명,출발,귀국,가격 from airline"
    cursor.execute(sql)
    data= []
    for row in cursor.fetchall():
        airline_data = {
            '항공명': row[0],
            '출발': row[1],
            '귀국': row[2],
            '가격': row[3]
        }
        data.append(airline_data)
    
    cursor.close()
    return jsonify(data)
    # return render_template('html.html',data_list=data_list)
    
if __name__=="__main__":
    #app.run(debug=True)
    # host 등을 직접 지정하고 싶다면
    app.run(use_reloader=False, host="127.0.0.1", port="80", debug=True)

# async def coroutine():
#     # Your asynchronous code goes here
#     await asyncio.sleep(1)
#     print("Coroutine has completed")

# loop = asyncio.get_event_loop()
# loop.run_until_complete(coroutine())
# loop.close()