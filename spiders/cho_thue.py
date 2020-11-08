import scrapy
from scrapy import Request
import json

class meeylandSpider(scrapy.Spider):
    name = "meeyland_chothue"
    url = 'https://api.meeyland.com/api/search'

    headers = {
        'authority': 'api.meeyland.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0',
        'content-type': 'application/json;charset=UTF-8',
        'origin': 'https://meeyland.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': "https://meeyland.com/cho-thue-nha-dat",
        'accept-language': 'en-US,en;q=0.9',
    }
    def start_requests(self):
        # temp = "Ho Chi Minh"
        # city_id = "5e5501caeb80a7245175de0c"
        # seo_url = temp.lower().replace(" ","-")
        # data = '{"category":"5deb722db4367252525c1d11","filter":"{\"attributes\":{\"5dfb2acdd5e511385e90df86\":[\"'+ city_id+'\"]},\"seoUrl\":\"'+seo_url+'\",\"date\":{\"startDate\":\"2001-01-19T17:00:00.000Z\",\"endDate\":\"2020-11-06T16:59:59.999Z\"}}","sort":"{\"createdDate\":-1}","skip":0,"limit":20,"search":""}'
        # data = '{"category":"5deb722db4367252525c1d00","filter":"{\\"attributes\\":{\\"5dfb2acdd5e511385e90df86\\":[\\"'+ city_id+'\\"]},\\"seoUrl\\":\\"'+seo_url+'\\",\\"date\\":{\\"startDate\\":\\"2001-01-19T17:00:00.000Z\\",\\"endDate\\":\\"2020-11-06T16:59:59.999Z\\"}}","sort":"{\\"createdDate\\":-1}","skip":0,"limit":20,"search":""}'
        # data = "{"category":"5deb722db4367252525c1d00","filter":"{\\"attributes\\":{\\"5dfb2acdd5e511385e90df86\\":[\\" + city_id + "\\"]},\\"seoUrl\\":\\"ho-chi-minh\\",\\"date\\":{\\"startDate\\":\\"2019-10-31T17:00:00.000Z\\",\\"endDate\\":\\"2020-11-01T16:59:59.999Z\\"}}","sort":"{\\"createdDate\\":-1}","skip":0,"limit":20,"search":""}"
        data = '{"category":"5deb722db4367252525c1d11","filter":"{\"attributes\":{\"5dfb2acdd5e511385e90df86\":[\"5e5501caeb80a7245175de0c\"]},\"seoUrl\":\"ho-chi-minh\",\"date\":{\"startDate\":\"2001-01-19T17:00:00.000Z\",\"endDate\":\"2020-11-08T16:59:59.999Z\"}}","sort":"{\"createdDate\":-1}","skip":0,"limit":20,"search":""}'
        yield Request(
            url=self.url,
            method='POST',
            dont_filter=True,
            headers=self.headers,
            body=data,
            callback=self.parse_page
        )

    def parse_page(self, response):
        data = json.loads(response.body)
        total_ads = 0
        if ('total' in data.keys()):
            if(int(data['total'])>0):
                total_ads = data['total']
            else:
                return
        number_page = round(total_ads/20)
        # temp = "Ho Chi Minh"
        # city_id = "5e5501caeb80a7245175de0c"
        # seo_url = temp.lower().replace(" ","-")
        for page in range(1,number_page+1):
            data ='{"category":"5deb722db4367252525c1d11","filter":"{\"attributes\":{\"5dfb2acdd5e511385e90df86\":[\"5e5501caeb80a7245175de0c\"]},\"seoUrl\":\"ho-chi-minh\",\"date\":{\"startDate\":\"2001-01-19T17:00:00.000Z\",\"endDate\":\"2020-11-08T16:59:59.999Z\"}}","sort":"{\"createdDate\":-1}","skip":'+str((page-1)*20)+',"limit":20,"search":""}'
            # data = '{"category":"5deb722db4367252525c1d11","filter":"{\"attributes\":{\"5dfb2acdd5e511385e90df86\":[\"'+ city_id+'\"]},\"seoUrl\":\"'+seo_url+'\",\"date\":{\"startDate\":\"2001-01-19T17:00:00.000Z\",\"endDate\":\"2020-11-06T16:59:59.999Z\"}}","sort":"{\"createdDate\":-1}","skip":'+str((page-1)*20)+',"limit":20,"search":""}'
            # data = '{"category":"5deb722db4367252525c1d00","filter":"{\\"attributes\\":{\\"5dfb2acdd5e511385e90df86\\":[\\"'+ city_id+'\\"]},\\"seoUrl\\":\\"'+seo_url+'\\",\\"date\\":{\\"startDate\\":\\"2001-01-19T17:00:00.000Z\\",\\"endDate\\":\\"2020-11-06T16:59:59.999Z\\"}}","sort":"{\\"createdDate\\":-1}","skip":'+str((page-1)*20)+',"limit":20,"search":""}'
            yield response.follow (
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
