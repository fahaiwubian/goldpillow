import scrapy
from tutorial.items import DouyuItem


class LagouSpider(scrapy.Spider):
    name = "lagou"
    allowed_domains = ['lagou.com']
    start_urls = [
        'https://www.lagou.com/'
    ]

    # def parse(self, response):
    #   for sel in response.xpath('//div[@class="pli_top"]'):
    #     # print(sel)
    #     tag = sel.xpath('div[@class="labels"]/div[@class="pli_btm_l"]/span/text()')[0].extract()
    #    print(tag)

    # def parse(self, response):
    #
    #     data = []
    #     for sel in response.xpath('//li[contains(@class,"position_list_item ")]'):
    #         item = LagouItem()
    #         item['positionName'] = sel.xpath('div/div[contains(@class,"pli_top_l")]/div/h2/a/text()')[0].extract()
    #         item['salary'] = sel.xpath('div/div[contains(@class,"pli_top_l")]/span/text()')[0].extract()
    #         item['experience'] = sel.xpath('div/div[contains(@class,"position_main_info")]/span/text()')[0].extract()
    #         item['education'] = sel.xpath('div/div[contains(@class,"position_main_info")]/span/text()')[1].extract()
    #         label = sel.xpath('div/div[@class="labels"]/div/span/text()').extract()
    #         item['label'] = ",".join(label)
    #         item['company'] = sel.xpath('div/div/div[contains(@class,"company_name")]/a/text()')[0].extract()
    #         item['companyType'] = sel.xpath('div/div/div[contains(@class,"industry ")]/span/text()')[0].extract()
    #         item['financing'] = sel.xpath('div/div/div[contains(@class,"industry ")]/span/text()')[1].extract()
    #         item['companyAddress'] = sel.xpath('div/div/div[contains(@class,"industry ")]/span/text()')[2].extract()
    #         item['imageUrl'] = sel.xpath('div/a/img/@src')[0].extract()
    #         data.append(item)
    #     return data

    def parse(self, response):
        for sel in response.xpath('//li[contains(@class,"position_list_item ")]'):
            item = DouyuItem()
            item['imglink'] = sel.xpath('div/a/img/@src')[0].extract().replace("//", "http://")

            yield item



