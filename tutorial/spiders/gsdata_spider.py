#-*- coding:utf-8 -*-
import sys
import re
import scrapy
from tutorial.items import GsdataItem
from scrapy.http import Request, FormRequest


reload(sys)
sys.setdefaultencoding('utf8')


class GsdataSpider(scrapy.Spider):


    name = "gsdata"
    #allowed_domains = ['gsdata.cn']

    start_urls = [
        'http://www.gsdata.cn/query/wx?q=lengiii',
        'http://www.gsdata.cn/query/wx?q=lengtoo',
        'http://www.gsdata.cn/query/wx?q=cxldb001',
        'http://www.gsdata.cn/query/wx?q=fgzadmin',
        'http://www.gsdata.cn/query/wx?q=lengxiaohua2012',
        'http://www.gsdata.cn/query/wx?q=iiiher',
        'http://www.gsdata.cn/query/wx?q=microhugo',
        'http://www.gsdata.cn/query/wx?q=yangongziyijinyexing',
        'http://www.gsdata.cn/query/wx?q=guanchacn',
        'http://www.gsdata.cn/query/wx?q=iiiread',
        'http://www.gsdata.cn/query/wx?q=ldgxsp',
        'http://www.gsdata.cn/query/wx?q=dongbeixiaopin',
        'http://www.gsdata.cn/query/wx?q=masee2013',
        'http://www.gsdata.cn/query/wx?q=miss_shopping_li',
        'http://www.gsdata.cn/query/wx?q=dujinyong6',
        'http://www.gsdata.cn/query/wx?q=qiubai2005',
        'http://www.gsdata.cn/query/wx?q=xd2299',
        'http://www.gsdata.cn/query/wx?q=wojiuaimoji',
        'http://www.gsdata.cn/query/wx?q=huazhuangshimk',
        'http://www.gsdata.cn/query/wx?q=rishi-ji',
        'http://www.gsdata.cn/query/wx?q=sixiangjujiao-weixin',
        'http://www.gsdata.cn/query/wx?q=jjtz999',
        'http://www.gsdata.cn/query/wx?q=thefair2',
        'http://www.gsdata.cn/query/wx?q=meiyajiejiemakiyo',
        'http://www.gsdata.cn/query/wx?q=love16po',
        'http://www.gsdata.cn/query/wx?q=carpwith',
        'http://www.gsdata.cn/query/wx?q=dacihua258',
        'http://www.gsdata.cn/query/wx?q=fcwm520',
        'http://www.gsdata.cn/query/wx?q=baobao90121',
        'http://www.gsdata.cn/query/wx?q=bomoda'
    ]
    # start_urls = []
    # file = open('C:/test-scrapy/tutorial/tutorial/url.txt')
    # for word in file:
    #     word = word.strip()
    #     url = 'http://www.gsdata.cn/query/wx?q=' + word
    #
    #     start_urls.append(url)

    headers = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip,deflate",
        "Accept-Language": "en-US,en;q=0.8,zh-TW;q=0.6,zh;q=0.4",
        "Connection": "keep-alive",
        "Content-Type": " application/x-www-form-urlencoded; charset=UTF-8",
        #"Referer": "http://www.gsdata.cn/member/login"
    }
    data = {
        'username': '17602136428',
        'password': '123456'
    }

    def start_requests(self):
        return [
            Request("http://www.gsdata.cn/member/login", meta={'cookiejar': 1}, callback=self.post_login)
        ]

    def post_login(self, response):
        return [
            FormRequest.from_response(response,
                                      meta={'cookiejar': response.meta['cookiejar']},
                                      headers=self.headers,
                                      formdata=self.data,
                                      callback=self.after_login
                                      )]

    def after_login(self, response):
        for url in self.start_urls:
            #print(url)
            yield self.make_requests_from_url(url)

    def parse(self, response):
        #data = []
        for sel in response.xpath('//div[@class="img-word"]'):
            item = GsdataItem()



            #item['nickname'] = sel.xpath('div/h1/a/span[@class="color-pink"]/text()')[0].extract()
            item['nickname'] = sel.xpath('div/h1/a//text()')[0].extract()
            wci = sel.xpath('div/h1/span[contains(@class,"wci")]/text()')[0].extract().replace("\r\n", " ")
            wci.strip()
            item['wci'] = wci.split("：")[1]
            item['wci'].replace(" ", "")
            item['wechat'] = sel.xpath('div[@class="word"]/p/span[@class="wxname"]/text()')[0].extract()
            types = sel.xpath('div[@class="word"]/p//text()')[2].extract()

            types.strip()
            typesData = types.split("：")
            type = typesData[1].replace("地区", " ")
            area = typesData[2].replace(" ", "")
            if area == "-":
                area = ""
            if type == "":
                type = ""

            #item['type'] = types[2].replace("\r\n", " ")
            item['type'] = type.replace(" ", "")
            item['area'] = area

            tag = sel.xpath('div/p[contains(@class,"mb0")]//text()').extract()
            del(tag[0])
            tag_all = []
            if tag:
                for index in tag:
                    if index.replace("\r\n", " ").strip() != "":
                        tag_all.append(index)
                item['tag'] = tag_all
            else:
                item['tag'] = tag


            # if tag:
            #     item['tag'] = ",".join(tag)
            # else:
            #     item['tag'] = ""
            item['desc'] = sel.xpath('div/div[contains(@class,"pro")]/p[contains(@class,"p-label")]/text()')[0].extract()
            imgUrl = sel.xpath('a/@style')[0].extract()
            img = re.findall(r'[^()]+', imgUrl)[1]
            item['imglink'] = img

            return item





           # print(desc)
            #item['desc'] = desc.extract()

            #item['type'] = sel.xpath('div/p/text()')[0].extract()
           # data.append(item['tag'])
        #return data






