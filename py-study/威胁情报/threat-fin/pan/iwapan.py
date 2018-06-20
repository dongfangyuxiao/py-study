#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 0026 下午 9:10
# @Author  : xiaodong
# @Site    : 
# @File    : iwapan.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'


# http://www.iwapan.com/so.aspx?wd=alibaba&pn=0&sstype=bd


from lib import myrequest
import re
req = myrequest
types = ['bd','360','huawei','xunlei','115'] #分别代表百度网盘、华为网盘、迅雷网盘、115网盘
print "Search now is in www.iwapan.com"
class iwangpan():
    def __init__(self,word,proxy=None):
        self.site_name = "www.iwapan.com"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "www.iwapan.com"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return
    def do_search(self):
        try:

            link = "http://{0}/so.aspx?wd={1}&pn=0&sstype={2}".format(self.server,self.word,self.type)
            print link
            r = req.get(link,proxies=self.proxies)
            self.results = r.content
            self.totalresults +=self.results
            return True
        except Exception,e:
            return False
    def process(self):
        for line in types:
            self.type = line
            self.do_search()

    def get_url(self):
        pattern = re.compile(r'<a href=(http.*?) target=') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        #return urls
        return urls


    def run(self):
        self.process()
        self.d = self.get_url()
        return self.d
if __name__ == "__main__":
    search = iwangpan("阿里巴巴")
    print search.run()
