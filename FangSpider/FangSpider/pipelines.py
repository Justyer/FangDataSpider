# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import scrapy
import pymongo

from collections import OrderedDict
from scrapy.exceptions import DropItem

from FangSpider.items import *

class FangspiderPipeline(object):
    def process_item(self, item, spider):
        return item

class JsonPipeline(object):

    def __init__(self):
        self.file = codecs.open('fang.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = ''

        new_item = FangItem()
        new_item['fang_title'] = item['fang_title'][0].strip()
        new_item['fang_danjia'] = item['fang_danjia'][0]
        new_item['fang_price'] = item['fang_price'][0]
        new_item['fang_shoufu'] = item['fang_shoufu'][0].strip()
        #new_item['fang_yuegong'] = item['fang_yuegong']
        new_item['fang_huxing'] = item['fang_huxing'][0].strip()
        new_item['fang_area'] = item['fang_area'][0]
        new_item['fang_ceng'] = item['fang_ceng'][0]
        new_item['fang_zxcd'] = item['fang_zxcd'][0]
        new_item['fang_face'] = item['fang_face'][0]
        new_item['fang_xiaoqu'] = item['fang_xiaoqu'][0]
        new_item['fang_region1'] = item['fang_region1'][0].strip()
        new_item['fang_region2'] = item['fang_region2'][0].strip()
        line += json.dumps(OrderedDict(new_item), ensure_ascii=False, sort_keys=False) + '\n'

        self.file.write(line)
        return new_item

class MongoPipeline(object):

    collection_name = 'fangdatacol'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
