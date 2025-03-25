import scrapy

class LinkSpider(scrapy.Spider):
    name = "link_spider"
    start_urls = ["http://quotes.toscrape.com/"]

    def parse(self, response):
        # 현재 페이지의 URL 출력
        self.logger.info(f"현재 탐색 중인 페이지: {response.url}")

        # 현재 페이지에서 이동할 수 있는 모든 링크(URL)를 추출
        urls = response.css("a::attr(href)").getall()
        
        # 상대 URL을 절대 URL로 변환하여 탐색
        for url in urls:
            yield response.follow(url, callback=self.parse_detail)

    def parse_detail(self, response):
        # 탐색 깊이(depth)를 확인하여 최대 5개 페이지까지만 탐색
        current_depth = response.meta.get('depth', 1)
        if current_depth > 5:
            return

        self.logger.info(f"{current_depth}번째 하위 페이지 탐색: {response.url}")

        # 현재 페이지에서 다시 URL을 추출하여 추가 탐색
        urls = response.css("a::attr(href)").getall()

        for url in urls:
            yield response.follow(url, callback=self.parse_detail)
