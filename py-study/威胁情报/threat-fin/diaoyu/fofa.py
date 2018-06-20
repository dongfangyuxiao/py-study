#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 上午 10:26
# @Author  : xiaodong
# @Site    : 
# @File    : fofa.py
# @Software: PyCharm
# fofa每个关键字默认查询一百条，超过后，就开始收费了，比较贵
__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

import os
import base64
from lib import config
from lib import myparser
import re
from lib import myrequest
req = myrequest

class search_fofa():
    def __init__(self, word):
        self.engine_name = "Fofa"
        try:
            self.email = config.FOFA_USER_EMAIL
            self.key = config.FOFA_API_KEY
        except:
            print "No Fofa Config,Exit"
            exit(0)
        self.word = word
        self.results = ""
        self.totalresults = ""
        self.server = "fofa.so"
        self.counter = 0 #useless
        self.print_banner()
        return

    def print_banner(self):
        print "Searching now in {0}..".format(self.engine_name)
        return
    def do_search(self):
        try:
            auth_url = "https://fofa.so/api/v1/info/my?email={0}&key={1}".format(self.email, self.key)
            auth = req.get(auth_url)
            query = base64.b64encode(self.word)
            url = "https://fofa.so/api/v1/search/all?email={0}&key={1}&qbase64={2}".format(self.email, self.key,
                                                                                           query)
            r = req.get(url)
            self.results = r.content
            #print r.content
            self.totalresults += self.results
            return True
        except Exception, e:
            print"Error in {0}: {1}".format(__file__.split('/')[-1],e)
            return False

    def get_hostnames(self):
        urls = []
        pattern = re.compile(r'\[\"(.*?)\"')
        urls_tem = pattern.findall(self.totalresults)
        for url in urls_tem:
            if 'http' not in url:
                url = 'http://' + url
            try:
                #print url
                res = req.get(url)
                if res.status_code:
                    urls.append(url)

            except Exception as e:
                print e



        return urls
    def process(self):
        self.do_search()
    def run(self): # define this function,use for threading, define here or define in child-class both should be OK
        try:
            self.process()
            self.d = self.get_hostnames()
            return self.d
        finally:
            print "{} found {} links ".format(self.engine_name, len(self.d))

if __name__ == "__main__":
        print "[-] Searching in fofa:"
        search = search_fofa("淘宝")
        print search.run()