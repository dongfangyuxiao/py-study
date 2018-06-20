#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 下午 3:46
# @Author  : xiaodong
# @Site    : 
# @File    : goofile.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

import subprocess
import re
import os
types = ['xls','txt','pdf','zip','7z','rar','doc','ppt','dot','log','ini','help']
class urlcrazy():
    def __init__(self,domain):
        self.tool = "urlcrazy"
        self.domain = domain
        self.domains = []
        self.email = []
        self.ip = []
        self.ipc = []
        self.results = ""
        return

    def system(self):

        try:
            print "Searching now is {}...".format(self.tool)
            a = subprocess.Popen('python goofile.py  -f '+ self.type + ' -d  ' + self.domain,shell=True
                                 ,stdout=subprocess.PIPE,cwd='/root/scan/xielou/goofile')
            data = a.stdout.readline()
            self.results+=data
        except Exception as e:
            print e

    def process(self):
        for type in types:
            self.type = type
            self.system()
    def get_url(self):
        urls = []
        for line in self.results:
            if self.domain in line:
                print line
                urls.append(line)
        return urls





    def run(self):
        self.d = self.get_url()



if __name__ == "__main__":
    search = urlcrazy("taobao.com")
    print search.run()