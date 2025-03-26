import scrapy
import re
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes_spider"
    start_urls = ["http://quotes.toscrape.com/js/page/1/"]

    def parse(self, response):
        script_text = response.xpath("//script[contains(., 'var data')]/text()").get()

        json_match = re.search(r'var\s+data\s*=\s*(\[\s*\{.*?\}\s*\]);', script_text, re.S)

        if json_match:
            json_text = json_match.group(1)
            quotes = json.loads(json_text)

            for quote in quotes:
                yield {
                    "text": quote["text"],
                    "author": quote["author"]["name"],
                    "author_link": quote["author"]["goodreads_link"],
                    "tags": quote["tags"]
                }
