#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 上午 11:51
# @Author  : xiaodong
# @Site    : 
# @File    : google.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

# 谷歌的反爬虫太厉害了，这个先不用了
from lib import myparser
import time
import random
from lib import myrequest
req = myrequest

class search_google():

    def __init__(self, word):
        self.engine_name = "Google"
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.files = "pdf"
        self.url = "https://www.google.com/search"
        self.quantity = "100"
        self.counter = 0
        return


    def do_search(self):
        try:
            url = "{0}?num={1}&start={2}&hl=en&meta=&q=inurl:{3}".format(self.url,self.quantity,self.counter,self.word)
            print url
            r = req.get(url)
            if "and not a robot" in r.content:
                print ("Google has blocked your visit")
                return False
            else:
                self.results = r.content
                self.totalresults += self.results
                return True
        except Exception, e:
            return False




    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()


    def process(self):
        while self.counter <= 1000:
            if self.do_search():
                time.sleep(random.randint(1, 5))  # should to sleep random time and use random user-agent to prevent block
                self.counter += 100
            else:
                break

    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        self.process()
        self.d = self.get_hostnames()
        return self.d

if __name__ == "__main__":
        print "[-] Searching in Google:"
        useragent = "Mozilla/5.0 (Windows; U; Windows NT 6.0;en-US; rv:1.9.2) Gecko/20100115 Firefox/3.6"  # 他会检查useragent，之前多了一个( 导致504
        search = search_google("taobao.com")
        print search.run()