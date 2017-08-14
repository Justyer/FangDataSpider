import re

from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request

from FangSpider.items import *

class SixSixProxySpider(CrawlSpider):
    name = 'xici_proxy_ip'
    start_urls = [
        'http://www.xicidaili.com/nn'
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
        self.website = 'http://www.xicidaili.com/'

    def start_requests(self):
        return [Request(
            self.start_urls[0],
            callback=self.get_page
        )]

    def get_page(self, response):
        ips = Selector(response).xpath('//*[@id="ip_list"]/tr/td[2]/text()').extract()
        print 'ips:',ips
        ports = Selector(response).xpath('//*[@id="ip_list"]/tr/td[3]/text()').extract()
        print 'ports:',ports
        item = IpItem()
        for ip, port in zip(ips, ports):
            print 'jljl:', ip, port
            item['table'] = 'xiciproxy'
            item['ip'] = str(ip)
            item['port'] = str(port)
            yield item

        next_page_url = Selector(response).xpath('//a[@class="next_page"]/@href').extract_first()
        yield Request(
            self.website + next_page_url,
            callback=self.get_page
        )
