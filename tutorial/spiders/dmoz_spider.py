import scrapy
from tutorial.items import DmozItem


class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ['haozu.com']
    start_urls = [
        "https://www.haozu.com/sh/pudongxinqu_yuqiaosq/"
    ]

    def parse(self, response):
        data = []
        for sel in response.xpath('//div[@class="list-content"]'):
            item = DmozItem()
            item['name'] = sel.xpath('h1[@class="h1-title"]/a/text()')[0].extract()
            item['price'] = sel.xpath('span[@class="s1"]/i[@class="i2"]/text()')[0].extract()
            #print(item['name'])
            #print(item['price'])
            data.append(item)
        return data




