#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 上午 9:54
# @Author  : xiaodong
# @Site    : 
# @File    : iask.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'
# http://ishare.iask.sina.com.cn/search/0-0-all-3-default?cond=%25E6%25B5%25A6%25E5%258F%2591%25E9%2593%25B6%25E8%25A1%258C
from lib import myrequest
import re
req = myrequest
import urllib
print "Search now is in www.ishare.iask.sina.com.cn"
class iask():
    def __init__(self,word,proxy=None):
        self.site_name = "ishare.iask.sina.com.cn"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "ishare.iask.sina.com.cn"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return

    def do_search(self):
        try:
            link = "http://{0}/search/0-0-all-{1}-default?cond={2}".format(self.server,self.counter,self.word)
            print link

            r = req.get(link,proxies=self.proxies)
            self.results = r.content
            self.totalresults +=  self.results
            return True
        except Exception,e:
            return False
    def process(self):
        for self.counter in range(1,11):#根据我的数次尝试，前10页足以
            self.do_search()
            self.counter += 1

    def get_url(self):
        pattern = re.compile(r'fl fl-title" href="(.*?)" onclick') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        urls =['http://ishare.iask.sina.com.cn' + x for x in urls]
        #return urls
        return urls


    def run(self):
        word_1 = urllib.quote(self.word)
        self.word = urllib.quote(word_1)  # 两次编码
        self.process()
        self.d = self.get_url()
        return self.d
if __name__ == "__main__":
    search = iask("阿里巴巴")
    print search.run()
