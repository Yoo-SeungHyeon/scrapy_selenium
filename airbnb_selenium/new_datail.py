from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
import time, json

# 크롤링할 탭 목록
target_tabs = ["통나무집", "최고의 전망", "캠핑장", "저택"]

options = Options()
# options.add_argument('--headless')  # 필요시 활성화
driver = webdriver.Chrome(options=options)
driver.get("https://www.airbnb.co.kr/")
wait = WebDriverWait(driver, 10)

results = []

# 숙소 목록을 감싸는 컨테이너의 selector
container_selector = "#site-content > div.f12t1m0s.atm_j3_1371zjx.atm_gw_1wugsn5.atm_lj_ke7zzc.atm_li_ke7zzc.atm_26_1p8m8iw.atm_8w_wetwqu.atm_vy_1osqo2v.atm_gp_1ixj6vq.f1scrphr.atm_go_h8pzn7.dir.dir-ltr > div.l14cupch.atm_h3_p5ox87.atm_h3_idpfg4_13mkcot.dir.dir-ltr > div > div > div > div"

for tab_name in target_tabs:
    try:
        # 탭 클릭
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[text()="{tab_name}"]')))
        tab.click()
        print(f"[+] '{tab_name}' 탭 클릭됨")

        # 로딩 대기
        time.sleep(10)

        # HTML 파싱
        html = driver.page_source
        sel = Selector(text=html)

        # 숙소 목록 컨테이너 선택
        container = sel.css(container_selector)
        if not container:
            print(f"[!] '{tab_name}' 탭에서 숙소 목록을 찾을 수 없음")
            continue

        container = container[0]

        # 숙소 리스트 항목들 (자식 div들)
        listings = container.css("div")
        listings_json = []

        for listing in listings:
            try:
                title = listing.css('[data-testid="listing-card-title"]::text').get()

                # 거리와 날짜 범위 추출
                subtitle_spans = listing.css('[data-testid="listing-card-subtitle"] span::text').getall()
                distance = subtitle_spans[0] if len(subtitle_spans) > 0 else None
                date_range = subtitle_spans[1] if len(subtitle_spans) > 1 else None

                # 가격
                price = listing.css('div[data-testid="price-availability-row"] span[class*="u1y3vocb"]::text').get()

                # 평점
                rating_spans = listing.css('div[class*="t1a9j9y7"] > span > span::text').getall()
                rating = rating_spans[-1] if rating_spans else None

                listings_json.append({
                    "title": title,
                    "price": price,
                    "date_range": date_range,
                    "distance": distance,
                    "rating": rating
                })

            except Exception as e:
                print(f"[!] 숙소 정보 추출 실패: {e}")



        results.append({
            "category": tab_name,
            "listings": listings_json
        })

    except Exception as e:
        print(f"[!] '{tab_name}' 탭 처리 중 오류: {e}")

driver.quit()

with open('airbnb_extracted_listings.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ JSON 저장 완료 → airbnb_extracted_listings.json")
