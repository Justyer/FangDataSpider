# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class FangItem(scrapy.Item):
    fang_title = scrapy.Field() #标题

    fang_danjia = scrapy.Field() #单价
    fang_price = scrapy.Field() #价格
    fang_shoufu = scrapy.Field() #首付
    #fang_yuegong = scrapy.Field() #月付

    fang_huxing = scrapy.Field() #户型
    fang_area = scrapy.Field() #建筑面积
    fang_ceng = scrapy.Field() #地上层数
    fang_zxcd = scrapy.Field() #装修程度
    fang_face = scrapy.Field() #进门朝向

    fang_xiaoqu = scrapy.Field() #小区
    fang_region1 = scrapy.Field() #区域1
    fang_region2 = scrapy.Field() #区域2

class IpItem(scrapy.Item):
    table = scrapy.Field()
    ip = scrapy.Field()
    port = scrapy.Field()
