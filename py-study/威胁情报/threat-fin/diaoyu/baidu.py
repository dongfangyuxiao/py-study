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


class search_baidu:

    def __init__(self, word, proxy=None):
        self.engine_name = "Baidu"
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.proxies = proxy
        self.server = "www.baidu.com"
        self.counter = 0  #
        self.print_banner()
        return

    def print_banner(self):
        print "Searching now in {0}..".format(self.engine_name)
        return
    def do_search(self):
        try:
            url = "http://{0}/s?wd=inurl%3A{1}&pn={2}".format(self.server, self.word, self.counter)  # 这里的pn参数是条目数
            r = req.get(url, proxies=self.proxies)
            self.results = r.content
            self.totalresults += self.results
            return True
        except Exception, e:
            return False

    def process(self):
        while self.counter <= 1000: #搜索前1000条
            if self.do_search():
                time.sleep(1)
                # print "\tSearching " + str(self.counter) + " results..."
                self.counter += 10
                continue
            else:
                break


    def get_hostnames(self):
        pattern = re.compile('text-decoration:none;">(.*?)</b>')
        rawres = pattern.findall(self.totalresults)
        urls = [x.replace('<b>','') for x in rawres]
        # print "%s domain(s) found in Baidu" %len(rawres.hostnames())
        return urls

    def run(self):  # define this function,use for threading, define here or define in child-class both should be OK
        try:
            self.process()
            self.d = self.get_hostnames()
            return self.d
        finally:
            print "{} found {} links ".format(self.engine_name, len(self.d))

if __name__ == "__main__":
    useragent = "(Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"
    proxy = {"http": "http://127.0.0.1:8080"}
    search = search_baidu("taobao.com")
    print search.run()

