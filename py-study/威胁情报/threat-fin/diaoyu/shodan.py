#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 上午 11:31
# @Author  : xiaodong
# @Site    :
# @File    : baidu.py
# @Software: PyCharm
# 利用搜索语法inurl:关键字，发现是否有钓鱼网站
__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

from lib import myparser
import re
import time
from lib import myrequest

req = myrequest

# https://www.shodan.io/search?query=apache
class search_shodan():

    def __init__(self, word, proxy=None):
        self.engine_name = "shodan"
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.proxies = proxy
        self.server = "www.shodan.io"
        self.counter = 0  #
        self.print_banner()
        return
    def print_banner(self):
        print "Searching now in {0}..".format(self.engine_name)
        return

    def do_search(self):
        try:
            url = "https://{0}/search?query={1}".format(self.server, self.word)  # 这里的pn参数是条目数
            r = req.get(url, proxies=self.proxies)
            self.results = r.content
            self.totalresults += self.results
            return True
        except Exception, e:
            return False

    def process(self):
        self.do_search()


    def get_hostnames(self):
        pattern = re.compile('class="ip"><a href="(.*?)">')
        urls = pattern.findall(self.totalresults)
        # print "%s domain(s) found in Baidu" %len(rawres.hostnames())
        return urls

    def run(self):  # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        return self.d


if __name__ == "__main__":
    useragent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
    proxy = {"http": "http://127.0.0.1:8080"}
    search = search_shodan("阿里巴巴")
    print search.run()

