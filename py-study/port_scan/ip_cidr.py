#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/2/7 0007 上午 9:25
# @Author  : xiaodong
# @Site    : 
# @File    : ip_cidr.py
# @Software: PyCharm
# 脚本的目的就是根据目录下的ip生成整个ip段的ip地址，然后可以通过shodan fofa zoomeye等看c段的地址开发的端口，查看有什么服务
#然后结合端口号进行下一步渗透，下一步的计划就是改成socket链接特定端口，判断是否开放，后续还要加入敏感目录扫描和漏洞扫描，然后再结合中间件扫描和jexboss，做成自动化
import threading
import requests
import config
from threading import  Thread
url_status = [200,302,403]
def creat_ip():
    f1 = open('ip.txt','rb')#输入你要扫描的ip段的一个ip就可以
    f2 = open('cidr.txt','wb')#生成的ip段
    for line in f1:
        line = line.strip()
        start = line.split('.')
        A = int(start[0])
        B = int(start[1])
        C = int(start[2])
        D = 0
        for D in range(1,256):
            ip = '%d.%d.%d.%d'%(A,B,C,D)
            f3 = open('port.txt', 'rb')#里面是根据乌云案例总结出的漏洞的常见漏洞的开放端口
            for line in f3:
                port = line.strip()
                url = 'http://' + ip + ':' + port
                f2.write(url + '\n')
def url_scan():
    f= open('cidr.txt','rb')
    f4 = open('url_scna.txt','wb')
    for line in f:
        url = line.strip()
        try:
            res = requests.get(url, headers=config.HEADER, timeout=config.TIMEOUT)
            status = res.status_code
            print status
            if status in url_status:
                f4.write(url + '\n')
                print url
        except:
            pass

if __name__ == "__main__":
    creat_ip()
    url_scan()
