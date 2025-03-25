from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import time

# 크롬 드라이버 자동 설치 및 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 시작 페이지
base_url = "https://quotes.toscrape.com/js/page/{}/"
page = 1

quotes_data = []

while True:
    url = base_url.format(page)
    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.quote"))
        )
    except Exception as e:
        print(f"페이지 {page} 로딩 실패 - 중단합니다.")
        break

    print(f"Page {page} 크롤링 중...")

    quotes_elements = driver.find_elements(By.CSS_SELECTOR, "div.quote")

    if not quotes_elements:
        print(f"Page {page}에 quote가 없습니다. 종료합니다.")
        break

    for quote in quotes_elements:
        text = quote.find_element(By.CSS_SELECTOR, "span.text").text
        author = quote.find_element(By.CSS_SELECTOR, "small.author").text
        tag_elements = quote.find_elements(By.CSS_SELECTOR, "div.tags a.tag")
        tags = [tag.text for tag in tag_elements]

        quotes_data.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    
    page += 1
    time.sleep(1)  


with open("output.json", "w", encoding="utf-8") as f:
    json.dump(quotes_data, f, ensure_ascii=False, indent=4)

print("모든 페이지 크롤링 완료- 'output.json'에 저장됐습니다.")
driver.quit()
