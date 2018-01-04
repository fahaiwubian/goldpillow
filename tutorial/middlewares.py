# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy import signals
from fake_useragent import UserAgent
#from tutorial.tools.crewler_ip import GetIp


## 随机更换user-agent
class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()
        self.ua = UserAgent()
        self.ua_type = crawler.settings.get("RANDOM_UA_TYPE", "random")

        #self.user_agent_list = crawler.settings.get("user_agent_list", [])

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            return getattr(self.ua, self.ua_type)
       # random_agent = get_ua()
        request.headers.setdefault("User-Agent", get_ua())


#动态设置ip代理
proxy_list = [
   "http://117.65.51.82:52311",
   "https://116.30.121.143:9000",
   "http://223.19.41.6:8380",
   "http://183.237.206.92:53281",
   "http://106.58.123.187:80",
   "http://118.193.107.147:80",
   "http://106.39.179.86:80",
   "http://116.199.115.79:82",
]


class RandomProxyMiddleware(object):
    def process_request(self, request, spider):
        proxy = self.get_random_proxy()
        print("this is request ip:" + proxy)
        request.meta['change_proxy'] = True
        request.meta['proxy'] = proxy

    def process_response(self, request, response, spider):

        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            proxy = self.get_random_proxy()
            print("this is response ip:" + proxy)
            # 对当前reque加上代理
            request.meta['change_proxy'] = True
            request.meta['proxy'] = proxy
            return request
        return response

    def get_random_proxy(self):
        proxy = random.choice(proxy_list).strip()
        #proxy = proxydata.get_random_ip()
        return proxy


class TutorialSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


