#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 0026 下午 8:42
# @Author  : xiaodong
# @Site    : 
# @File    : lingfen.py
# @Software: PyCharm
# 凌风搜索这个需要登录，所以正则匹配到的url是凌风本站点的，以后再看怎么修改，资源的跳转需要购买vip
__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'
# https://www.lingfengyun.com/search?wd=alibaba&select_so=1&page=2
import sys
sys.path.append('../')
from lib import myrequest
import re
req = myrequest
types = ['project','code','issues','user']
print "Search now is in www.lingfengyun.com"
class lingfen():
    def __init__(self,word,proxy=None):
        self.site_name = "www.lingfengyun.com"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "www.lingfengyun.com"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return
    def do_search(self):
        try:

            link = "https://{0}/search?wd={1}&select_so=1&page={2}".format(self.server,self.word,self.counter)
            print link
            r = req.get(link,proxies=self.proxies)
            self.results = r.content
            self.totalresults +=self.results
            return True
        except Exception,e:
            return False
    def process(self):
        for self.counter in range(1,6):#根据我的数次尝试，前5页足以
            self.do_search()
            self.counter += 1

    def get_url(self):
        pattern = re.compile(r'<a href="(https://www.lingfengyun.com/.*?)" target="_blank">') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        #return urls
        return urls


    def run(self):
        self.process()
        self.d = self.get_url()
        print "{} found {}".format(self.server, len(self.d))
        return self.d

if __name__ == "__main__":
    search = lingfen("阿里巴巴")
    print search.run()
