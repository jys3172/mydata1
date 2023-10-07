from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=chrome_options)

#웹페이지 해당 주소 이동
driver.get("http://flight.naver.com/")
time.sleep(3)


driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[1]/button[2]').click()
time.sleep(1)

driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[10]/div[1]/div/input').send_keys('오사카')
time.sleep(1)
driver.find_element(By.CLASS_NAME, 'autocomplete_airport__3zusQ').click()


driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/div[2]/button[1]').click()
time.sleep(1)

driver.find_elements(By.XPATH, '//b[text() = "21"]')[0].click()
time.sleep(1)

driver.find_elements(By.XPATH, '//b[text() = "24"]')[1].click()
time.sleep(0)

driver.find_elements(By.XPATH, '//*[@id="__next"]/div/div/div[4]/div/div/div[2]/button')[0].click()
time.sleep(5)


# concurrent_ConcurrentItemContainer__2lQVG result
# 항공사: airline
# 출발 route_Route__2UInh[0]
# 도착 route_Route__2UInh[1]
# 가격 item_firstItem__15zkv

results = driver.find_elements(By.CLASS_NAME,'concurrent_ConcurrentItemContainer__2lQVG.result')
for result in results:
    try:
        airline = result.find_element(By.CLASS_NAME, 'airline').text
        startTime = result.find_elements(By.CLASS_NAME, 'route_Route__2UInh')[0].text.replace('\n', ' ')
        returnTime = result.find_elements(By.CLASS_NAME, 'route_Route__2UInh')[1].text.replace('\n', ' ')
        price = result.find_element(By.CLASS_NAME, 'item_firstItem__15zkv').text.replace('\n', ' ')
        print(f'항공사 : {airline}')
        print(f'출발 : {startTime}')
        print(f'귀국 : {returnTime}')
        print(f'가격 : {price}')
        print('-'*100)
    except:
        pass

input()