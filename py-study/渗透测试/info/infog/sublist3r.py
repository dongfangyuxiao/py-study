#!/usr/bin/python
# -*- coding:utf-8 -*-
# for:
# user:xiaodong
# usage:
# tool:pycharm

import subprocess


from config import myparse
import os

class sublist3r():
    def __init__(self,domain):
        self.tool = "sublist3r"
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
            a = subprocess.Popen('python sublist3r.py  -o /root/project/info/sublist3r.txt  -d ' + self.domain,shell=True
                                 ,stdout=subprocess.PIPE,cwd='/root/info/subdomain/Sublist3r')
            b = a.stdout.readlines()
            #print b



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
            f = open('/root/project/info/sublist3r.txt', 'rb')
            for line in f:
                self.results += line
            self.d = self.get_domain()
            self.e = self.get_emails()
            self.ips = self.get_ips()
            self.ipcs = self.get_ipcs()

        finally:
            print "{} is over found {} domains {} emails".format(self.tool,len(self.d),len(self.e))
            return self.d,self.e,self.ips,self.ipcs



if __name__ == "__main__":
    search = sublist3r("taobao.com")
    print search.run()



