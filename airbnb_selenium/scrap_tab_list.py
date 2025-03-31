from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scrapy.selector import Selector
import time

# 크롬 옵션 설정 (headless는 필요에 따라 켜고 끌 수 있어요)
options = Options()
options.add_argument('--headless')  # 브라우저 안 띄움
options.add_argument('--disable-gpu')

# 드라이버 실행
driver = webdriver.Chrome(options=options)

# URL 열기
driver.get('https://www.airbnb.co.kr/')

# 잠시 대기 (JS 실행 시간 확보)
time.sleep(3)

# 페이지 소스를 Scrapy Selector로 래핑
sel = Selector(text=driver.page_source)


# 텍스트 목록 추출
texts = sel.css('#categoryScroller label span span::text').getall()

for text in texts:
    print(text)


# # 모든 a 태그 href 가져오기
# hrefs = sel.css('a::attr(href)').getall()

# # 결과 출력
# print(hrefs)

# # 텍스트 추출
# text = sel.css('div.t192ua0c span::text').get()
# print(text)


# 드라이버 종료
driver.quit()
