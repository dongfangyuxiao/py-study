#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 上午 9:50
# @Author  : xiaodong
# @Site    : 
# @File    : slimego.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'
# http://www.slimego.cn/search.html?q=%E6%B5%A6%E5%8F%91%E9%93%B6%E8%A1%8C&page=2&rows=20&v=0.50716237446168
import sys
sys.path.append('../')
from lib import myrequest
import re
req = myrequest
print "Search now is in slimego"
class slimego():
    def __init__(self,word,proxy=None):
        self.site_name = "www.slimego.cn"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "www.slimego.cn"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return
    def do_search(self):
        try:

            link = "http://{0}/search.html?q={1}&page={2}&rows=20&v=0.50716237446168".format(self.server,self.word,self.counter)
            #print link
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
        urll = []
        pattern = re.compile(r'a rel="noreferrer" href="(.*?)"') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        for url in urls:
            resqq = req.get(url)

            urll.append(url)
        return urll



    def run(self):
        self.process()
        self.d = self.get_url()
        print "{} found {}".format(self.server, len(self.d))
        return self.d
#if __name__ == "__main__":
    #search = slimego("阿里巴巴")
    #print search.run()

