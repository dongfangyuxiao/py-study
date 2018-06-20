#!/usr/bin/python
# -*- coding:utf-8 -*-
# for:
# user:xiaodong
# usage:
# tool:pycharm

import re

class parse():
    def __init__(self,results,word):
        self.results = results
        self.word = word
        self.tmp = []

    def emails(self):
        reg_emails = re.compile('[a-zA-Z0-9.\-_+#~!$&,;=:]+' +
            '@' +
            '[a-zA-Z0-9.-]*' +
            self.word)
        self.tmp = reg_emails.findall(self.results)
        emails = self.unique()
        return emails

    def domains(self):
        reg_domains = re.compile('[a-zA-Z0-9]'+'[a-zA-Z0-9.-]*\.' + self.word)
        self.tmp = reg_domains.findall(self.results)
        domains = self.unique()
        return  domains

    def ips(self):
        reg_ips = re.compile('\d+\.\d+\.\d+\.\d+')
        self.tmp = reg_ips.findall(self.results)
        ips = self.unique()
        return ips

    def ipcs(self):
        reg_ipc = re.compile('\d+\.\d+\.\d+\.\d+\/\d+')
        self.tmp = reg_ipc.findall(self.results)
        ipcs = self.unique()
        return ipcs

    def unique(self):
        self.new = []
        for x in self.tmp:
            if ".." in x:
                pass
            elif x not in self.new:
                self.new.append(x)
        return self.new

if __name__ == "__main__":
    print ("XX")