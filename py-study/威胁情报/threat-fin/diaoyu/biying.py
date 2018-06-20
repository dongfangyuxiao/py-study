#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 上午 11:51
# @Author  : xiaodong
# @Site    : 
# @File    : biying.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'
# !/usr/bin/env python
# -*- coding:utf-8 -*-
__author__ = 'bit4'
__github__ = 'https://github.com/bit4woo'


from lib import myparser
import time
from lib import myrequest
req = myrequest
import re
class search_bing:

    def __init__(self, domain, proxy=None):
        self.engine_name = "Bing"
        self.domain = domain.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.url = "https://cn.bing.com/search"
        self.limit = 1000
        self.counter = 0
        self.headers = {"Cookie":"SRCHHPGUSR=ADLT=DEMOTE&NRSLT=50","Accept-Language":"'en-us,en"}
        self.proxies = proxy
        self.print_banner()
        return

    def print_banner(self):
        print "Searching now in {0}..".format(self.engine_name)
        return

    def do_search(self):
        url = "{0}?q=site:{1}&count=50&first={2}".format(self.url, self.domain, self.counter)  # 这里的pn参数是条目数
        r = req.get(url, headers = self.headers, proxies = self.proxies)
        self.results = r.content
        self.totalresults += self.results


    def do_search_vhost(self):
        url = "{0}q=ip:{1}&go=&count=50&FORM=QBHL&qs=n&first={2}".format(self.url,self.ip,self.counter)


    def get_hostnames(self):
        pattern = re.compile('<a target="_blank" href="(.*?)" h="')
        urls = pattern.findall(self.totalresults)
        return urls

    def process(self):
        while (self.counter < self.limit):
            if self.do_search():
                #self.do_search_vhost()
                time.sleep(1)
                self.counter += 50
                continue
            else:
                break
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        try:
            self.process()
            self.d = self.get_hostnames()
            return self.d
        finally:
            print "{} found {} links ".format(self.engine_name, len(self.d))

if __name__ == "__main__":
        print "[-] Searching in Bing:"
        search = search_bing("taobao.com")
        print search.run()