from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
import json
import time
import traceback

# 크롤링할 Airbnb 탭 이름들
target_tabs = ["통나무집", "최고의 전망", "캠핑장", "저택"]

# 크롬 옵션 설정
options = Options()
# options.add_argument('--headless')  # 실제 운영 시 사용 가능
driver = webdriver.Chrome(options=options)
driver.get("https://www.airbnb.co.kr/")
wait = WebDriverWait(driver, 30)

results = []

for tab_name in target_tabs:
    try:
        # 탭 클릭
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[text()="{tab_name}"]')))
        driver.execute_script("arguments[0].scrollIntoView(true);", tab)
        tab.click()
        print(f"[+] '{tab_name}' 탭 클릭됨")

        # 숙소가 충분히 로드될 때까지 스크롤 + 대기
        def enough_listings_loaded(driver):
            sel = Selector(text=driver.page_source)
            return len(sel.css('[data-testid="property-card"]')) >= 20


        wait.until(enough_listings_loaded)
        print(f"[+] 숙소 5개 이상 로드됨")

        # HTML 파싱
        html = driver.page_source
        sel = Selector(text=html)
        listings = sel.css('[data-testid="property-card"]')

        listings_json = []

        for listing in listings:
            try:
                title = listing.css('[data-testid="listing-card-title"]::text').get()

                subtitle = listing.css('[data-testid="listing-card-subtitle"] span::text').getall()
                distance = subtitle[0] if len(subtitle) > 0 else None
                date_range = subtitle[1] if len(subtitle) > 1 else None

                price = listing.css('[data-testid="price-availability-row"] span::text').re_first(r'₩[\d,]+')
                rating = listing.css('[aria-label*="점 만점에"]::text').get()

                if any([title, price, date_range, distance, rating]):
                    listings_json.append({
                        "title": title,
                        "price": price,
                        "date_range": date_range,
                        "distance": distance,
                        "rating": rating
                    })

            except Exception as e:
                print(f"[!] 숙소 정보 추출 실패: {e}")

        print(f"📦 '{tab_name}' 탭 → {len(listings_json)}개 숙소 크롤링 완료")
        results.append({
            "category": tab_name,
            "listings": listings_json
        })

    except Exception as e:
        print(f"[!] '{tab_name}' 탭 처리 중 오류 발생:")
        traceback.print_exc()

        # 디버깅용 HTML 저장
        with open(f'debug_{tab_name}.html', 'w', encoding='utf-8') as f:
            f.write(driver.page_source)

driver.quit()

# JSON 저장
with open('airbnb_detail.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ JSON 저장 완료 → airbnb_detail.json")
