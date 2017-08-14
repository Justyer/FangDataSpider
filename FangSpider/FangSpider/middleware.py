# -*- coding: UTF-8 -*-

import time
import logging as log
import random
import re

from proxy import PROXIES, FREE_PROXIES
from agents import AGENTS
from selenium import webdriver
from scrapy.http import HtmlResponse

class CustomHttpProxyFromMongoMiddleware(object):
    proxies = FREE_PROXIES

    def process_request(self, request, spider):

        def __init__(self):
            self.psy_db = 'proxypool'
            self.psy_password = '495495'
            self.psy_host = '127.0.0.1'
            self.psy_port = '5432'
            self.conn = psycopg2.connect(database=self.psy_db, user='postgres', password=self.psy_password, host=self.psy_host, port=self.psy.port)
            self.cur = conn.cursor()

        random_id = random.random(1, self.sur.rowcount)
        self.cur = execute('select ip,port from proxypool where id=%d' % random_id)
        p = self.cur.fetchone()[0]
        try:
            request.meta['proxy'] = "http://%s:%s" % (p.ip, p.port)
            print(request.meta['proxy'])
        except Exception, e:
            #log.msg("Exception %s" % e, _level=log.CRITICAL)
            log.critical("Exception %s" % e)

class CustomUserAgentMiddleware(object):
    def process_request(self, request, spider):
        agent = random.choice(AGENTS)
        request.headers['User-Agent'] = agent

class SeleniumMiddleware(object):
    def process_request(self, request, spider):
        if re.match(r'http://www.kuaikanmanhua.com', request.url) is not None:
            print 'Chrome is starting...'
            driver = webdriver.Chrome()
            driver.get(request.url)
            for i in range(1, 70):
                js = 'document.body.scrollTop=%d' % (i*500)
                driver.execute_script(js)
                time.sleep(0.1)
            body = driver.page_source
            return HtmlResponse(driver.current_url, body=body, encoding='utf-8', request=request)
