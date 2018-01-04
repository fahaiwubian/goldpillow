import scrapy


class HuxiuSpider(scrapy.Spider):
    name = "huxiu"
    allowed_domains = ['xncoding.com']
    start_urls = [
        "https://www.xncoding.com/2016/03/10/scrapy-02.html"
    ]

    def parse(self, response):
        for sel in response.xpath('//ol[@class="nav"]/li[@class="nav-item nav-level-2"]'):
            num = sel.xpath('a/span[@class="nav-number"]/text()')[0].extract()
            title = sel.xpath('a/span[@class="nav-text"]/text()')[0].extract()
            print(num, title)
