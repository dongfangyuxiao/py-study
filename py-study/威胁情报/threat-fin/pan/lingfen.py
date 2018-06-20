#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 0026 下午 8:42
# @Author  : xiaodong
# @Site    : 
# @File    : lingfen.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'
# https://www.lingfengyun.com/search?wd=alibaba&select_so=1&page=2

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
        for self.counter in range(1,11):#根据我的数次尝试，前5页足以
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
        return self.d
if __name__ == "__main__":
    search = lingfen("阿里巴巴")
    print search.run()
