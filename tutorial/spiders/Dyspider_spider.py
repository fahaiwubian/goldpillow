import scrapy
import json
from tutorial.items import DouyuItem


class DyspiderSpider(scrapy.Spider):
    name = 'dyspider'
    allowed_domains = ['douyucdn.cn']
    allowed_domains = ['lagou.com']
    start_urls = [
        'https://www.lagou.com/'
    ]

    def parse(self, response):
        for sel in response.xpath('//li[contains(@class,"position_list_item ")]'):
            item = DouyuItem()
            item['imglink'] = sel.xpath('div/a/img/@src')[0].extract()
            print item['imglink']