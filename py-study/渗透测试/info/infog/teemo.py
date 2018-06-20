#!/usr/bin/python
# -*- coding:utf-8 -*-
# for:
# user:xiaodong
# usage:
# tool:pycharm

import subprocess



from config import myparse
import os

class teemo():
    def __init__(self,domain):
        self.tool = "teemo"
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
            a = subprocess.Popen('python teemo.py -o /root/project/info/teemo.txt -d ' + self.domain,shell=True
                                 ,stdout=subprocess.PIPE,cwd='/root/info/subdomain/teemo')
            b = a.stdout.readlines()
            #print b


            return self.results
        except Exception as e:
            print e

    def get_domain(self):
        rawres =myparse.parse(self.results,self.domain)
        return rawres.domains()

    def get_ips(self):
        rawres = myparse.parse(self.results, self.domain)
        return rawres.ips()

    def get_ipcs(self):
        rawres = myparse.parse(self.results, self.domain)
        return rawres.ipcs()

    def get_emails(self):
        rawres = myparse.parse(self.results, self.domain)
        return rawres.emails()


    def run(self):
        try:
            self.system()
            f = open('/root/project/info/teemo.txt', 'rb')
            for line in f:
                self.results += line
            self.d = self.get_domain()
            self.e = self.get_emails()
            self.ips = self.get_ips()
            self.ipcs = self.get_ipcs()
        finally:
            print "{} found {} domains {} emails {} ip {} ipc".format(self.tool, len(self.d), len(self.e),
                                                                      len(self.ips),
                                                                      len(self.ipcs))
            return self.d,self.e,self.ips,self.ipcs

if __name__ == "__main__":
    search = teemo("taobao.com")
    print search.run()


