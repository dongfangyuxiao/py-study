#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 上午 10:26
# @Author  : xiaodong
# @Site    : 
# @File    : fanlian.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

from lib import myparser
import re
import time
from lib import myrequest

req = myrequest
# https://link.aizhan.com/index.php?r=site%2Findex&url=taobao.com&vt=a&linktext=&page=3
# 正则匹配 翻页 <a href="javascript:void(0);"
class search_fanlian:

    def __init__(self, word, proxy=None):
        self.engine_name = "fanlian"
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.proxies = proxy
        self.server = "link.aizhan.com"
        self.counter = 1  #
        self.print_banner()
        return

    def print_banner(self):
        print "Searching now in {0}..".format(self.engine_name)
        return

    def do_search(self):
        try:
            url = "https://{0}/index.php?r=site%2Findex&url={1}&vt=a&linktext=&page={2}".format(self.server, self.word, self.counter)  # 这里的pn参数是条目数
            #print url
            r = req.get(url, proxies=self.proxies)
            self.results = r.content
            #print self.results
            self.totalresults += self.results
            return True
        except Exception, e:
            print e

    def check_next(self):
        renext = re.compile('<a href="javascript:void(.*?);"')
        nextres = renext.findall(self.results)
        if nextres != []:
            #print "ok"
            return True
        else:
            return False


    def process(self):
        while (self.counter < 10):  # limit = item number; counter= page number ... 10 items per page
            if self.do_search():
                if self.check_next():
                    self.counter += 1
                    continue
                else:
                    break
            else:
                break


    def get_hostnames(self):
        pattern = re.compile('"owner title"><a href="(.*?)" target="_blank" ')
        urls = pattern.findall(self.totalresults)
        # print "%s domain(s) found in Baidu" %len(rawres.hostnames())
        return urls

    def run(self):  # define this function,use for threading, define here or define in child-class both should be OK
        try:
            self.process()
            self.d = self.get_hostnames()
            return self.d
        finally:
            print "{} found {} links ".format(self.engine_name, len(self.d))



if __name__ == "__main__":
    search = search_fanlian("taobao.com")
    print search.run()

