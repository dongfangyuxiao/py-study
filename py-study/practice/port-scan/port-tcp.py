#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  18-6-23 上午8:06
# Author :  xiaodong
# File   :  port-tcp.py

#一个多线程的tcp端口扫描器，，定义了两个函数

import argparse
import socket
from socket import *
from threading import *
screenlock = Semaphore(value=1)

def connScan(tgtHost,tgtPort):# 这个主要是进行端口扫描，进行tcp链接，获取一些信息

    try:
        connskt = socket(AF_INET,SOCK_STREAM)# 创建一个socket 对象family的取值通常是AF_INET。type 的取值通常是SOCK_STREAM(用于定向的连接，可靠的TCP连接)或SOCK_DGRAM(用于UDP)
        connskt.connect((tgtHost,tgtPort))
        connskt.send('hello word\r\n')
        result = connskt.recv(100)
        screenlock.acquire()
        print "{} open  and found {}".format(tgtPort,result)
    except:
        screenlock.acquire()
        print "sorry, {} closed".format(tgtPort)
    finally:
        screenlock.release()
        connskt.close()

def portscan(tgtHost,tgtPorts):# 这个主要是进行主机名的变换，并且多线程调用connScan函数
    try:
        tgtIp = gethostbyname(tgtHost)#gethostbyname(name) 尝试将给定的主机名解释为一个IP地址。
    except:
        print "cannot resolve {}".format(tgtHost)
        return
    try:
        tgtName = gethostbyaddr(tgtIp)#gethostbyaddr() 由IP 地址得到DNS 信息，返回一个类似gethostbyname_ex()的3 元组。
        print "scan result for {}".format(tgtName[0])
    except:
        print "scan result for {}".format(tgtIp)
    setdefaulttimeout(1)
    for tgtPort in tgtPorts:
        t = Thread(target=connScan,args=(tgtHost,int(tgtPort)))
        t.start()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host',help='please input what you want to scan host,eg:www.baidu.com')
    parser.add_argument('port',help='please input port what you want to scan,eg:21,22')
    args = parser.parse_args()

    tgtHost = args.host

    tgtPorts = str(args.port).split(',')
    if (tgtHost == None) | (tgtPorts ==None):
        print " are you sure you input is right?"
        exit(0)
    portscan(tgtHost,tgtPorts)


if __name__ == "__main__":
    main()





