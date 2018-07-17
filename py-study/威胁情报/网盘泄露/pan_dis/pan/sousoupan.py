#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  2018/5/14 0014 上午 10:21
# Author :  xiaodong
# File   :  sousoupan.py
import sys
sys.path.append('../')
from lib import myrequest

import re

req = myrequest

print "Search now is in sosuopan"
# http://www.sosuopan.com/search?q=%E6%B5%A6%E5%8F%91%E4%BF%A1%E7%94%A8%E5%8D%A1&pn=2
class sosuopan():
    def __init__(self,word,proxy=None):
        self.site_name = "www.sosuopan.com"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "www.sosuopan.com"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return
    def do_search(self):
        try:

            link = "http://{0}/search?q={1}&pn={2}".format(self.server,self.word,self.counter)
            #print link
            r = req.get(link,proxies=self.proxies)
            self.results = r.content
            self.totalresults +=self.results
            return True
        except Exception,e:
            return False
    def process(self):
        for self.counter in range(1,4):#根据我的数次尝试，前3页足以
            self.do_search()
            self.counter += 1

    def get_url(self):
        urll = []
        pattern = re.compile(r'object-link fpm" href="(.*?)"') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        #return urls
        for url in urls:#此时匹配到的url是sosuopan的链接，转换为百度云盘链接
            resp = req.get(url)
            uu0 = re.findall(r'a href="(.*?)" target="_blank"',resp.content)
            uu = uu0[0]
            ressp = req.get(uu)
            if 'platform-non-found' not in ressp.content:

                urll.append(uu)

        return urll


    def run(self):
        self.process()
        self.d = self.get_url()
        print "{} found {}".format(self.server, len(self.d))
        return self.d

#if __name__ == "__main__":

    #search = sosuopan("阿里巴巴")
    #print search.run()