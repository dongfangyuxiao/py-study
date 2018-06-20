#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15 0015 下午 1:11
# @Author  : xiaodong
# @Site    :
# @File    : github.py
# @Software: PyCharm
# 从githu上利用github高级搜索语法，进行搜索
__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'
import requests
from lib import config
from lib import myrequests
req = myrequests
import re
from bs4 import BeautifulSoup
print "Search now is in oschain"
types =['all','project','bbs','blog','code','translate','news'] #oschina 查找的类型
cookie = ""
class oschina():
    def __init__(self,word,proxy=None):
        self.engine_name = 'oschina'
        self.result = "" #本页搜索结果
        self.totalresult = "" #全部搜索结果
        self.server = 'www.oschina.net'
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = ""
        self.word = word.replace(' ','%20')
        return



    def do_search(self):
        try:
            url = "https://{0}/search?scope={1}&q={2}&p={3}".format(self.server,self.type,self.word,self.counter)
            print url
            r = req.get(url)
            self.result = r.content
            self.totalresult +=self.result
            return True
        except Exception, e:
            return False
    def check_next(self):
        renext = re.compile('">(.*?)gt;</a></li>')
        nextres = renext.findall(self.result)
        if nextres !=[]:
            nexty = "1"
        else:
            nexty = "0"
        return nexty
    def process(self):
        for type in types:
            self.type = type
            for self.counter in range(1,2):
                self.do_search()

    def get_url(self):
        pattern_all = re.compile('</em><a href=\'(.*?)\' target=')
        pattern_project = re.compile('<h3><a href=\'(.*?)\' target=')
        pattern_blog = re.compile('<p class=\'url\'>\'(.*?)\'</p>')
        urls1 = pattern_all.findall(self.totalresult)
        urls2 = pattern_project.findall(self.totalresult)
        urls3 = pattern_blog.findall(self.totalresult)
        urls = urls1+urls2+urls3
        #for url in urls:
            #print url
        if urls:
            return urls
        else:return False


    def run(self):
        self.process()
        self.d = self.get_url()
        return self.d


if __name__ == "__main__":
    seach = oschina("alibaba")
    seach.run()