import scrapy
import json
from scrapy import Request

class meeyland_provinceSpider(scrapy.Spider):
    name = "meeyland_province"
    
    def start_requests(self):
        base_url = 'https://api.meeyland.com/api/city'
        headers = {
            'authority': 'api.meeyland.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json, text/plain, */*',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'content-type': 'application/json;charset=UTF-8',
            'origin': 'https://meeyland.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://meeyland.com/mua-ban-nha-dat',
            'accept-language': 'en-US,en;q=0.9',
        }

        yield Request(
            url=base_url,
            method='POST',
            dont_filter=True,
            headers=headers,
            callback=self.parse_city
        )
    def parse_city(self,response):
        data = json.loads(response.body)
        for city in data:
            yield {
                city["_id"]:city["englishName"]
            }

