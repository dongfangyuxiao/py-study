#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  2018/5/14 0014 上午 10:21
# Author :  xiaodong
# File   :  fx.py

import sys
sys.path.append('../')
from lib import myrequest
from bs4 import BeautifulSoup
import re
req = myrequest
print "Search now is in 57fx"
class fx():
    def __init__(self,word,proxy=None):
        self.site_name = "www.57fx.com"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "www.57fx.com"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        self.url1 = []
        return
    def do_search(self):

        try:

            link = "https://{0}/search-all-{1}-{2}/".format(self.server,self.word,self.counter)
            #print link
            r = req.get(link,proxies=self.proxies)
            self.results = r.content
            res = BeautifulSoup(self.results, "lxml")
            urls = res.findAll('dd')
            for i in urls:
                i = i.find('a')
                self.url1.append(i['href'])
            return True
        except Exception,e:
            return False
    def process(self):
        for self.counter in range(1,10):#根据我的数次尝试，前5页足以
            self.do_search()
            self.counter += 1

    def get_url(self):
        urll =[]

        url1 = ['https://www.57fx.com'+x for x in self.url1]
        for line in url1:
            try:
                resp = req.get(line)
                uu0 = re.findall(r'href="(.*?)" target="_blank" name=',resp.content)
                uu = uu0[0]

                urll.append(uu)
            except Exception as e:
                pass
        return urll


    def run(self):
        self.process()
        self.d = self.get_url()
        print "{} found {}".format(self.server, len(self.d))
        return self.d

#if __name__ == "__main__":
    #search = fx("浦发信用卡")
    #print search.run()