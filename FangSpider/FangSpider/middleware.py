# -*- coding: UTF-8 -*-

import time
import logging as log
import random
import re

from proxy import PROXIES, FREE_PROXIES
from agents import AGENTS
from selenium import webdriver
from scrapy.http import HtmlResponse

class CustomHttpProxyFromMysqlMiddleware(object):
    proxies = FREE_PROXIES

    def process_request(self, request, spider):
        # TODO implement complex proxy providing algorithm
        if self.use_proxy(request):
            p = random.choice(self.proxies)
            try:
                request.meta['proxy'] = "http://%s" % p['ip_port']
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
