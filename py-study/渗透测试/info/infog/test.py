#!/usr/bin/python
# -*- coding:utf-8 -*-
# for:
# user:xiaodong
# usage:
# tool:pycharm

import os

import subprocess

import re
results = str(0)
f = open('/root/project/info/fierce.txt')
for line in f:
    results +=line
reg_ips = re.compile('\d+\.\d+\.\d+\.\d+')
ips = reg_ips.findall(results)
#for ip in ips:
    #print ip

reg_ipcs = re.compile('(\d+\.\d+\.\d+\.0-255)')
ipcs = reg_ipcs.findall(results)
for line in ipcs:
    print line
reg_domains = re.compile('[a-zA-Z0-9]'+'[a-zA-Z0-9.-]*\.'+'spdbccc.com.cn')
domains = reg_domains.findall(results)
#for line in domains:
    #print line

reg_emails = re.compile('[a-zA-Z0-9.\-_+#~!$&,;=:]+' +
            '@' +
            '[a-zA-Z0-9.-]*' +
            'spdbccc.com.cn')
emails = reg_emails.findall(results)
#for email in emails:
    #print email

fie_ipcs = re.compile('')