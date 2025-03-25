import scrapy


class BasicTestSpider(scrapy.Spider):
    name = "basic_test"
    allowed_domains = ["basic_test.py"]
    start_urls = ["https://basic_test.py"]

    def parse(self, response):
        pass
