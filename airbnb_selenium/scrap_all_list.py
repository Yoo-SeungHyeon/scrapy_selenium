from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
import time, json

def element_to_json(element):
    node = {"tag": element.tag}
    if element.attrib:
        node["attributes"] = dict(element.attrib)
    
    children = []
    if element.text and element.text.strip():
        children.append(element.text.strip())
    
    for child in element:
        children.append(element_to_json(child))
        if child.tail and child.tail.strip():
            children.append(child.tail.strip())
    
    if children:
        node["children"] = children
    return node

# 크롤링할 탭 목록
target_tabs = ["통나무집", "최고의 전망", "캠핑장", "저택"]

options = Options()
# options.add_argument('--headless')
driver = webdriver.Chrome(options=options)
driver.get("https://www.airbnb.co.kr/")
wait = WebDriverWait(driver, 20)

results = []

# 숙소 목록을 감싸는 컨테이너의 selector
container_selector = "#site-content > div.f12t1m0s.atm_j3_1371zjx.atm_gw_1wugsn5.atm_lj_ke7zzc.atm_li_ke7zzc.atm_26_1p8m8iw.atm_8w_wetwqu.atm_vy_1osqo2v.atm_gp_1ixj6vq.f1scrphr.atm_go_h8pzn7.dir.dir-ltr > div.l14cupch.atm_h3_p5ox87.atm_h3_idpfg4_13mkcot.dir.dir-ltr > div > div > div > div"

for tab_name in target_tabs:
    try:
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[text()="{tab_name}"]')))
        tab.click()
        print(f"[+] '{tab_name}' 탭 클릭됨")
        time.sleep(20)  # 로딩 대기

        html = driver.page_source
        sel = Selector(text=html)
        
        # 숙소 목록 컨테이너 선택
        container = sel.css(container_selector)
        if not container:
            print(f"[!] '{tab_name}' 탭에서 컨테이너를 찾을 수 없음")
            continue

        container = container[0]  # 첫 번째 (유일한) 컨테이너
        
        # 자식 숙소 div 모두 선택
        listings = container.css("div")  # 직접 자식만 선택

        listings_json = [element_to_json(listing.root) for listing in listings]

        results.append({
            "category": tab_name,
            "listings": listings_json
        })

    except Exception as e:
        print(f"[!] '{tab_name}' 탭 처리 중 오류: {e}")

driver.quit()

with open('airbnb_listings_by_tab.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ JSON 저장 완료 → airbnb_listings_by_tab.json")
