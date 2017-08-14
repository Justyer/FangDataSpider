import re

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from FangSpider.items import *

class NianshaoProxySpider(CrawlSpider):
    name = 'nianshao_proxy_ip'
    start_urls = [
        'http://www.nianshao.me/'
    ]
    custom_settings = {
        #'MONGO_URI': 'mongodb://127.0.0.1:27017',
        #'MONGO_DATABASE': 'fangip',
        'ITEM_PIPELINES':{
           #'FangSpider.pipelines.MongoPipeline': 300,
           'FangSpider.pipelines.PostgreSQLPipeline': 300,
        }
    }

    def __init__(self):
        self.website = 'http://www.nianshao.me/'
        self.page = 1
        self.next_page_url = 'http://www.nianshao.me/?page='

    def start_requests(self):
        return [Request(
            self.start_urls[0],
            callback=self.get_page
        )]

    def get_page(self, response):
        if self.page <= 157:
            self.page += 1
            yield Request(
                self.next_page_url + str(self.page),
                callback=self.get_page
            )

            ips = Selector(response).xpath('//tbody/tr/td[1]/text()').extract()
            ports = Selector(response).xpath('//tbody/tr/td[2]/text()').extract()
            item = IpItem()
            for ip, port in zip(ips, ports):
                item['table'] = 'nianshaoproxy'
                item['ip'] = str(ip)
                item['port'] = str(port)
                yield item
