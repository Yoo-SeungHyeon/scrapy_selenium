import scrapy

class LinkSpider(scrapy.Spider):
    name = "link_spider"
    start_urls = ["http://quotes.toscrape.com/"]
    
    def parse(self, response):
        current_depth = response.meta.get('depth', 0)
        
        # 현재 방문한 페이지의 정보 저장
        yield {
            'depth': current_depth,
            'url': response.url,
            'referer': response.request.headers.get('Referer', None).decode() if response.request.headers.get('Referer') else None
        }

        # 다음 탐색할 URL들을 추출 및 탐색
        if current_depth < 5:
            urls = response.css("a::attr(href)").getall()
            for url in urls:
                yield response.follow(url, callback=self.parse)
