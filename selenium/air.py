from selenium import webdriver
import time

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

#크롬 드라이버 자동 업데이트
from webdriver_manager.chrome import ChromeDriverManager

#브라우저 꺼짐 방지
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

#불필요한 에러 메세지 없애기
chrome_options.add_experimental_option("excludeSwitches",["enable-logging"])

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service,options=chrome_options)

# 스크롤 다운 함수
def scroll_down():
    SCROLL_PAUSE_SEC = 1
    # 스크롤 높이 가져옴
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 끝까지 스크롤 다운
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 1초 대기
        time.sleep(SCROLL_PAUSE_SEC)

        # 스크롤 다운 후 스크롤 높이 다시 가져옴
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


if __name__ == '__main__':
    # 네이버 항공권 사이트 접속
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service,options=chrome_options)

    driver.get('https://flight.naver.com/flights/?'
               'trip=OW&scity1=TAE&ecity1=CJU&adult=1&child=0&infant=0&fareTy'
               'pe=YC&airlineCode=&nxQuery=%ED%95%AD%EA%B3%B5%EA%B6%8C')

    # 날짜 선택란 클릭
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div[1]/fieldset/div[2]/div[1]/div/div[1]/a").click()
    time.sleep(1)

    # 날짜 선택 - input 형식으로 숫자를 받아서 html 주소에 숫자를 넣을 것임.
    # 월 선택
    months = ['이번 달', '다음 달']
    for i, month in enumerate(months):
        print(f'{i + 1}. {month}\t', end='\t')
    print()
    monthInput = int(input("몇월에 떠나시나요? : "))
    print()

    # 주 선택
    weeks = ['첫째 주', '둘째 주', '셋째 주', '넷째 주', '다섯째 주', '여섯째 주']
    for i, week in enumerate(weeks):
        print(f'{i + 1}. {week}\t', end='\t')
    print()
    weekInput = int(input("몇째 주에 떠나시나요? : "))
    print()

    # 요일 선택
    days = ['일', '월', '화', '수', '목', '금', '토']
    for i, day in enumerate(days):
        print(f'{i + 1}. {day}\t', end='\t')
    print()
    dayInput = int(input("무슨 요일에 떠나시나요? : "))
    print()

    # 지정한 날짜 선택하기 - input 을 통해 원하는 html 주소 (날짜 선택) 를 클릭.
    driver.find_element_by_xpath(f"/html/body/div/div/div[2]/div[1]/"
                                 f"fieldset/div[2]/div[1]/div/div[3]/"
                                 f"div/div[2]/div[1]/div/div[{monthInput}]/"
                                 f"div[2]/table/tbody/tr[{weekInput}]/td[{dayInput}]/a").click()


    # 항공권 검색 클릭
    driver.find_element_by_xpath("/html/body/div/div/div[2]/div[1]/fieldset/a").click()
    time.sleep(4)

    # 출발 시간항목 지정
    departure_time = ['전체', '00:00 ~ 06:00', '06:00 ~ 09:00', '09:00 ~ 12:00',
                      '12:00 ~ 15:00', '15:00 ~ 18:00', '18:00 ~ 24:00']

    for i, d_time in enumerate(departure_time):
        print(f"{i + 1}. {d_time}", end='\t')

    print()
    timeInput = int(input("출발 시간을 선택하세요 : "))
    print()

    # 출발 시간 선택
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]/div/div[2]/ul/li[2]/a/span[1]").click()
    if timeInput == 1:
        driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                     "/div/div[2]/ul/li[2]/div/ul/li[1]/span").click()
        # 시간항목이 전체일 경우 : 스크롤 다운 함수 실행
        scroll_down()

    elif timeInput == 2:
        driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                     "/div/div[2]/ul/li[2]/div/ul/li[2]/span").click()
    elif timeInput == 3:
        driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                     "/div/div[2]/ul/li[2]/div/ul/li[3]/span").click()
    elif timeInput == 4:
        driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                     "/div/div[2]/ul/li[2]/div/ul/li[4]/span").click()
    elif timeInput == 5:
        driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                     "/div/div[2]/ul/li[2]/div/ul/li[5]/span").click()
    elif timeInput == 6:
        driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                     "/div/div[2]/ul/li[2]/div/ul/li[6]/span").click()
    elif timeInput == 7:
        driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]"
                                     "/div/div[2]/ul/li[2]/div/ul/li[7]/span").click()


    flights = driver.find_element_by_xpath("/html/body/div/div/div[1]/div[2]/div[2]/div/div[4]")
    info = flights.text  
    flight_list = info.split()
    print(flight_list)

    price_list = []

    print()
    print("<< 시간 순 >>")
    # 항공사, 출발 시각, 가격 -> 내가 필요한 정보만 추출하기 위한 슬라이싱
    for i in range(len(flight_list)-1):

        if flight_list[i] == '제주항공':
            # 항공사 / 출발 시간 / 가격 출력력
            print(f'{flight_list[i]}\t\t\t{flight_list[i + 3]}\t\t{flight_list[i + 13]}')
            price_list.append([flight_list[i], flight_list[i + 3], flight_list[i + 13]])

        elif flight_list[i] =='티웨이항공':
            print(f'{flight_list[i]}\t\t{flight_list[i + 3]}\t\t{flight_list[i + 13]}')
            price_list.append([flight_list[i], flight_list[i + 3], flight_list[i + 13]])

        elif flight_list[i] == '진에어':
            print(f'{flight_list[i]}\t\t\t{flight_list[i + 3]}\t\t{flight_list[i + 13]}')
            price_list.append([flight_list[i], flight_list[i + 3], flight_list[i + 13]])

        elif flight_list[i] == '아시아나항공':
            print(f'{flight_list[i]}\t\t{flight_list[i + 3]}\t\t{flight_list[i + 13]}')
            price_list.append([flight_list[i], flight_list[i + 3], flight_list[i + 13]])

    print()

    for i in price_list:
        # price_list 속 가격을 int 화 시키기
        str_price = i[2]
        price = str_price[:-1]
        price = int(price.replace(',', ''))

        # int 화 시킨 가격으로 리스트 다시 작성
        i.insert(0, price)

    sort_price_list = sorted(price_list)

    print()
    print("<< 가격 낮은 순 >>")
    for i in sort_price_list:
        # print(i)
        if i[1] == '제주항공':
            print(f'{i[1]}\t\t\t{i[2]}\t\t{i[3]}')
        elif i[1] == '티웨이항공':
            print(f'{i[1]}\t\t{i[2]}\t\t{i[3]}')
        elif i[1] == '진에어':
            print(f'{i[1]}\t\t\t{i[2]}\t\t{i[3]}')
        elif i[1] == '아시아나항공':
            print(f'{i[1]}\t\t{i[2]}\t\t{i[3]}')

    driver.close()