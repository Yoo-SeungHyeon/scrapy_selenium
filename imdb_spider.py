import scrapy
import json

class ImdbSpider(scrapy.Spider):
    name = "imdb"
    start_urls = ["https://www.imdb.com/chart/top/"]
    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'User-Agent': 'Mozilla/5.0'
        }
    }

    def parse(self, response):
        json_data = response.xpath("//script[@type='application/ld+json']/text()").get()
        data = json.loads(json_data)

        for movie in data['itemListElement']:
            yield {
                'title': movie['item']['name'],
                'url': movie['item']['url'],
                'rating': movie['item']['aggregateRating']['ratingValue']
            }
