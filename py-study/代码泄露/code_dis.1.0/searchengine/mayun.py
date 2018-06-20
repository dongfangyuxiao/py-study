#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 0014 上午 10:46
# @Author  : xiaodong
# @Site    : 
# @File    : mayun.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

import requests
from lib import myrequests
import re
req = myrequests
types = ['project','code','issues','user']
print "Search now is in mayun"
class mayun():
    def __init__(self,word,proxy=None):
        self.site_name = "mayun"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "gitee.com"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return
    def do_search(self):
        try:

            link = "https://{0}/search?condition=default&language=&page={1}&search={2}&type={3}".format(self.server,self.counter,self.word,self.type)
            print link
            r = req.get(link,proxies=self.proxies)
            self.results = r.content
            self.totalresults +=self.results
            return True
        except Exception,e:
            return False
    def process(self):
        for self.counter in range(1,11):#码云的结果准确度太低，所以只取前十页
            for type in types:
                self.type = type
                self.do_search()
            self.counter += 1

    def get_url(self):
        pattern = re.compile(r'<a href="(.*?)" target="_blank"><strong>') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        #return urls
        urls = ['https://gitee.com'+url for url in urls]
        if urls :
            return urls
        else: return False
    def get_title(self): # 获取title目前，失败了，回头再看
        links = self.get_url()
        for link in links:
            r=req.get(link,proxies=self.proxies).content
            pattern = re.compile(r'<title>(.*?)</title>')
            title = re.search(pattern,r)
            print title
    def run(self):
        self.process()
        self.d = self.get_url()
        return self.d
if __name__ == "__main__":
    search = mayun("alibaba")
    print search.run()



