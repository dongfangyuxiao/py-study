#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 0026 下午 7:54
# @Author  : xiaodong
# @Site    : 
# @File    : panduoduo.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

import sys
sys.path.append('../')
from lib import myrequest

import re
req = myrequest
types = ['project','code','issues','user']
print "Search now is in panduoduo"
class panduoduo():
    def __init__(self,word,proxy=None):
        self.site_name = "www.panduoduo.net"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "www.panduoduo.net"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return
    def do_search(self):
        try:

            link = "http://{0}/s/name/{1}/{2}".format(self.server,self.word,self.counter)
            #print link
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
        urll = []
        pattern = re.compile(r'href="(/r/.*?)"') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        #return urls
        urls = ['http://www.panduoduo.net'+x for x in urls]
        for url in urls:#此时匹配到的url是panduoduo的链接，转换为百度云盘链接
            resp = req.get(url)
            uu0 = re.findall(r'class="dbutton2" href="(.*?)"',resp.content)
            uu = uu0[0]
            try:
                resqq = req.get(uu)
                url1 = re.findall(r'var url = "(.*?)";', resqq.content)


                urll.append(url1[0])
            except Exception as e:
                pass

        return urll


    def run(self):
        self.process()
        self.d = self.get_url()
        return self.d
        print "{} found {}".format(self.server, len(self.d))
if __name__ == "__main__":
    search = panduoduo("阿里巴巴")
    print search.run()










