# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


#class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
  #  pass

class DmozItem(scrapy.Item):
    name = scrapy.Field()
    price = scrapy.Field()


class LagouItem(scrapy.Item):
    positionName = scrapy.Field()
    salary = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    label = scrapy.Field()
    company = scrapy.Field()
    companyType = scrapy.Field()
    financing = scrapy.Field()
    companyAddress = scrapy.Field()
    imageUrl = scrapy.Field()


class MyItem(scrapy.Item):

    image_urls = scrapy.Field()  #保存图片地址
    images = scrapy.Field()      #保存图片的信息


class DouyuItem(scrapy.Item):

    imglink = scrapy.Field()
   # image_paths = scrapy.Field()
    pass


class GsdataItem(scrapy.Item):
     nickname = scrapy.Field()   # 昵称
     wechat = scrapy.Field()    # 微信号
     type = scrapy.Field()      #分类
     area = scrapy.Field()      #地区
     tag = scrapy.Field()       #标签
     wci = scrapy.Field()       #wci
     desc = scrapy.Field()      #功能介绍
     imglink = scrapy.Field()    #头像地址
