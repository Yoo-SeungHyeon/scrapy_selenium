from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.selector import Selector
import time, json

def element_to_json(element):
    """
    lxml element를 재귀적으로 순회하여 태그, 속성, 자식 노드(태그 및 텍스트)를 JSON 형태의 dict로 변환합니다.
    """
    node = {"tag": element.tag}
    if element.attrib:
        node["attributes"] = dict(element.attrib)
    
    children = []
    # element.text: 태그 내부의 텍스트(있을 경우)
    if element.text and element.text.strip():
        children.append(element.text.strip())
    
    # 자식 노드 순회
    for child in element:
        children.append(element_to_json(child))
        # 태그 뒤의 텍스트(있을 경우)
        if child.tail and child.tail.strip():
            children.append(child.tail.strip())
    
    if children:
        node["children"] = children
    return node

# 크롤링할 탭 목록
target_tabs = ["통나무집", "최고의 전망", "캠핑장", "저택"]

options = Options()
# options.add_argument('--headless')  # 브라우저를 직접 확인하고 싶으면 주석 해제하지 않음
driver = webdriver.Chrome(options=options)
driver.get("https://www.airbnb.co.kr/")
wait = WebDriverWait(driver, 10)

results = []

for tab_name in target_tabs:
    try:
        # 탭 클릭: 지정한 탭이 클릭 가능할 때까지 대기 후 클릭
        tab = wait.until(EC.element_to_be_clickable((By.XPATH, f'//span[text()="{tab_name}"]')))
        tab.click()
        print(f"[+] '{tab_name}' 탭 클릭됨")
        
        # 탭 클릭 후 충분한 로딩을 위해 대기 (예: 10초)
        time.sleep(10)
        
        # 현재 페이지의 HTML을 Scrapy Selector로 파싱
        html = driver.page_source
        sel = Selector(text=html)
        
        # sel.root는 lxml Element 객체를 반환하므로 재귀 함수로 JSON 변환
        html_structure = element_to_json(sel.root)
        
        results.append({
            "category": tab_name,
            "html_structure": html_structure
        })
    except Exception as e:
        print(f"[!] '{tab_name}' 탭 처리 중 오류: {e}")

driver.quit()

with open('airbnb_tabs_structure.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("✅ JSON 저장 완료 → airbnb_tabs_structure.json")
