#!/usr/bin/python
# -*- coding:utf-8 -*-
# for:
# user:xiaodong
# usage:
# tool:pycharm
# 脚本的作用
# 1、对于信息收集发现的ip、和域名进行http探测，查看能否访问，利用request 生成http.txt
# 2、对 ipc段发现的所有ip进行端口扫描，利用工具为masscna，对可以通过http访问的也加入到http.txt用于后续漏洞扫描和敏感目录扫描
# 3、对于2不能通过http访问的，生成一个其他的文件no_http,能访问的用whatweb指纹识别
import subprocess
import re

import requests

import threading

import myrequest as req

class scan():
    def __init__(self):
        self.tool = "masscan port scan"
        self.domain_http = []
        self.http = []
        self.no_http = []
        self.ip_port = []



    def masscan(self):
        try:
            print "Searching now is {}...".format(self.tool)
            a = subprocess.Popen('masscan -p1-9999 --rate 10000 -oL /root/project/info/masscan.txt -iL /root/project/info/ipc_all.txt',
                                 shell=True
                                 , stdout=subprocess.PIPE, cwd='/root/project/info')
            b = a.stdout.readlines()

        except Exception as e:
            print e
            pass
    def port(self):
        self.masscan()
        f = open('/root/project/info/masscan.txt', 'rb')
        for line in f:
            try:
                line = line.split(' ')
                ip_port = str(line[3]) + str(':') + str(line[2])
                self.ip_port.append(ip_port)
            except Exception as e:
                print e
                pass
        f_portscan = open('/root/project/info/port/portscan.txt','wb')
        f_portscan.writelines("\n".join(self.ip_port).encode("utf-8"))
        # print b
        return self.ip_port
    def verity_http(self):
        self.port()
        http = []
        http_ok = [200,302,404,500]
        f= open('/root/project/info/port/portscan.txt','rb')
        f_http = open('/root/project/info/port/http.txt','wb')
        f_no_http = open('/root/project/info/port/no_http.txt', 'wb')
        f_domain = open('/root/project/info/domain_all.txt','rb')
        f_ip = open('/root/project/info/domain_all.txt', 'rb')
        for line in f:
            line = line.strip()
            http.append(line)
        for line in f_domain:
            line = line.strip()
            http.append(line)
        for line in f_ip:
            line  = line.strip()
            http.append(line)
        for line in http:
            if '443' in line:
                url = 'https://'+line+'/'
            else:
                url = 'http://'+line+'/'
            try:
                res = req.get(url)
                if res.status_code:
                    print "{} http is ok".format(url)
                    self.http.append(url)
                    f_http.write(url +'\n')
            except Exception as e:
                print "sorry,this not http"
                f_no_http.write(line +'\n')
    def whatweb(self):
        self.verity_http()
        try:

            a = subprocess.Popen('whatweb -i /root/project/info/port/http.txt --log-json /root/project/info/port/whatweb.json',shell=True, stdout=subprocess.PIPE, cwd='/root/project/info')
            b = a.stdout.read()

        except Exception as e:
            print e
            pass








    def run(self):
        self.whatweb()
        print "port scan is all over"

if __name__:
    x = scan()
    print x.run()

