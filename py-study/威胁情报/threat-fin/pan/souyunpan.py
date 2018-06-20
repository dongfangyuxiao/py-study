#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 0026 下午 9:41
# @Author  : xiaodong
# @Site    : 
# @File    : souyunpan.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

# http://www.soyunpan.com/search/alibaba-0-%E5%85%A8%E9%83%A8-0.html

from lib import myrequest
import re
req = myrequest
print "Search now is in souyunpan"
class souyunpan():
    def __init__(self,word,proxy=None):
        self.site_name = "www.soyunpan.com"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "www.soyunpan.com"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return
    def do_search(self):
        try:

            link = "http://{0}/search/{1}-0-%E5%85%A8%E9%83%A8-{2}.html".format(self.server,self.word,self.counter)
            print link
            r = req.get(link,proxies=self.proxies)
            self.results = r.content
            self.totalresults +=self.results
            return True
        except Exception,e:
            return False
    def process(self):
        for self.counter in range(1,10):#根据我的数次尝试，前5页足以
            self.do_search()
            self.counter += 1

    def get_url(self):
        pattern = re.compile(r'href="(.*?)"><font style') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        #return urls
        return urls


    def run(self):
        self.process()
        self.d = self.get_url()
        return self.d
if __name__ == "__main__":
    search = souyunpan("阿里巴巴")
    print search.run()

