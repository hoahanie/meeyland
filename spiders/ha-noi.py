import scrapy
from scrapy import Request
import json

class meeylanSpider(scrapy.Spider):
    name = "meeyland_hanoi"
    url = 'https://api.meeyland.com/api/search'

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
        'referer': "https://meeyland.com/mua-ban-nha-dat",
        'accept-language': 'en-US,en;q=0.9',
    }
    def start_requests(self):

        temp = "Ha Noi"
        city_id = "5e5501caeb80a7245175dddb"
        seo_url = temp.lower().replace(" ","-")
        data = '{"category":"5deb722db4367252525c1d00","filter":"{\\"attributes\\":{\\"5dfb2acdd5e511385e90df86\\":[\\"'+ city_id+'\\"]},\\"seoUrl\\":\\"'+seo_url+'\\",\\"date\\":{\\"startDate\\":\\"2001-01-19T17:00:00.000Z\\",\\"endDate\\":\\"2020-11-01T16:59:59.999Z\\"}}","sort":"{\\"createdDate\\":-1}","skip":0,"limit":20,"search":""}'
        # data = "{"category":"5deb722db4367252525c1d00","filter":"{\\"attributes\\":{\\"5dfb2acdd5e511385e90df86\\":[\\" + city_id + "\\"]},\\"seoUrl\\":\\"ho-chi-minh\\",\\"date\\":{\\"startDate\\":\\"2019-10-31T17:00:00.000Z\\",\\"endDate\\":\\"2020-11-01T16:59:59.999Z\\"}}","sort":"{\\"createdDate\\":-1}","skip":0,"limit":20,"search":""}"
        yield Request(
            url=self.url,
            method='POST',
            dont_filter=True,
            headers=self.headers,
            body=data,
            # meta= {
            #     "city_id": city_id,
            #     "seo_url": seo_url
            # },
            callback=self.parse_page
        )

    def parse_page(self, response):
        data = json.loads(response.body)
        total_ads = data["total"]
        # region = response.meta["region"]
        # city_id = response.meta["city_id"]
        # seo_url = response.meta["seo_url"]
        temp = "Ha Noi"
        city_id = "5e5501caeb80a7245175dddb"
        seo_url = temp.lower().replace(" ","-")

        number_page = round(total_ads/20)
        for page in range(1,number_page+1):
            data = '{"category":"5deb722db4367252525c1d00","filter":"{\\"attributes\\":{\\"5dfb2acdd5e511385e90df86\\":[\\"'+ city_id+'\\"]},\\"seoUrl\\":\\"'+seo_url+'\\",\\"date\\":{\\"startDate\\":\\"2001-01-19T17:00:00.000Z\\",\\"endDate\\":\\"2020-11-01T16:59:59.999Z\\"}}","sort":"{\\"createdDate\\":-1}","skip":'+str((page-1)*20)+',"limit":20,"search":""}'
            yield Request(
                url=self.url,
                method='POST',
                dont_filter=True,
                headers=self.headers,
                body=data,
                callback=self.parse_ads
            )

    def parse_ads(self,response):
        data = json.loads(response.body)
        yield {
            "data": data
        }

