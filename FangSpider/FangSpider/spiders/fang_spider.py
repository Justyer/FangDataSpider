import re

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from FangSpider.items import *

class FangSpider(CrawlSpider):
    name = 'fang'
    start_urls = [
        'http://esf.fang.com/'
    ]
    custom_settings = {
        'MONGO_URI': 'mongodb://127.0.0.1:27017',
        'MONGO_DATABASE': 'fangdata',
        'ITEM_PIPELINES':{
           'FangSpider.pipelines.JsonPipeline': 300,
           'FangSpider.pipelines.MongoPipeline': 400,
        }
    }

    def __init__(self):
        self.website = 'http://esf.fang.com/'

    def start_requests(self):
        return [Request(
            self.start_urls[0],
            callback=self.get_list
        )]

    def get_list(self, response):
        fang_urls = Selector(response).xpath('//*[@class="houseList"]/dl/dt/a/@href').extract()
        if fang_urls is not None:
            for url in fang_urls:
                yield Request(
                    self.website + url,
                    callback=self.get_info
                )

        next_page_url = Selector(response).xpath('//*[@id="PageControl1_hlk_next"]/@href').extract_first()
        print 'next_page_url:' + next_page_url
        if next_page_url is not None:
            yield Request(
                self.website + next_page_url,
                callback=self.get_list
            )

    def get_info(self, response):
        l = ItemLoader(item=FangItem(), response=response)
        l.add_xpath('fang_title', '//*[@id="lpname"]/text()')
        l.add_xpath('fang_danjia', '/html/body/div[5]/div[1]/div[3]/div[3]/div[3]/div[1]/text()')
        l.add_xpath('fang_price', '/html/body/div[5]/div[1]/div[3]/div[2]/div[1]/i/text()')
        l.add_xpath('fang_shoufu', '/html/body/div[5]/div[1]/div[3]/div[2]/div[2]/text()')
        #l.add_xpath('fang_yuegong', '//*[@id="FirstYG"]/text()')
        l.add_xpath('fang_huxing', '/html/body/div[5]/div[1]/div[3]/div[3]/div[1]/div[1]/text()')
        l.add_xpath('fang_area', '/html/body/div[5]/div[1]/div[3]/div[3]/div[2]/div[1]/text()')
        l.add_xpath('fang_ceng', '/html/body/div[5]/div[1]/div[3]/div[4]/div[2]/div[1]/text()')
        l.add_xpath('fang_zxcd', '/html/body/div[5]/div[1]/div[3]/div[4]/div[3]/div[1]/text()')
        l.add_xpath('fang_face', '/html/body/div[5]/div[1]/div[3]/div[4]/div[1]/div[1]/text()')
        l.add_xpath('fang_xiaoqu', '//*[@id="agantesfxq_C03_05"]/text()')
        l.add_xpath('fang_region1', '//*[@id="agantesfxq_C03_07"]/text()')
        l.add_xpath('fang_region2', '//*[@id="agantesfxq_C03_08"]/text()')
        yield l.load_item()
