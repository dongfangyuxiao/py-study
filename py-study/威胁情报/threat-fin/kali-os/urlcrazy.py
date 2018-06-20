#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 下午 3:39
# @Author  : xiaodong
# @Site    : 
# @File    : urlcrazy.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

#!/usr/bin/python
# -*- coding:utf-8 -*-
# for:
# user:xiaodong
# usage:
# tool:pycharm

import subprocess
import re
import os

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
            a = subprocess.Popen('urlcrazy  -o /root/project/info/xielou/urlcrazy.txt  ' + self.domain,shell=True
                                 ,stdout=subprocess.PIPE,cwd='/root/info/subdomain/subDomainsBrute')
            b = a.stdout.readlines()
        except Exception as e:
            print e

    def get_domain(self):
        urls = []
        f = open('/root/project/info/xielou/urlcrazy.txt','rb')
        for line in f:
            c = re.search(r'\w+(\.\w+)(\.\w+)(\.\w+)', line)
            if c!=0:
                ip = re.search(r'\w+(\.\w+)(\.\w+)(\.\w+)', line)
                domain = re.search(r'\w+(\.\w+)+', line)
                url = ip + ' '+domain
                urls.append(url)
        return urls




    def run(self):
        try:
            self.system()
            f = open('/root/project/info/subDomainsBrute.txt', 'rb')
            for line in f:
                self.results += line
            self.d = self.get_domain()

        finally:
            print "{} found {} domains {} emails {} ip {} ipc".format(self.tool, len(self.d))
            return self.d


if __name__ == "__main__":
    search = urlcrazy("taobao.com")
    print search.run()