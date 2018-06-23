#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  18-6-23 上午9:54
# Author :  xiaodong
# File   :  port-nmap.py

import  nmap
#(此处导入的nmap 为python-nmap)

import argparse

# https://www.cnblogs.com/aylin/p/5996229.html
# AttributeError: 'function' object has no attribute 'PortScanner'  如果出现这个，说明安装错了，要安装python-nmap
def nmapScan(tgtHost,tgtPort):
    nmscan = nmap.PortScanner()
    nmscan.scan(tgtHost,tgtPort)
    state = nmscan[tgtHost]['tcp'][int(tgtPort)]['state']#获取主机  端口（tcp）的状态 （open|closed|filter）
    print "{} found {}".format(tgtHost,state)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host',help='input ip you want to scan')
    parser.add_argument('port',help='scan port')
    args = parser.parse_args()

    tgtHost = args.host
    tgtPorts = str(args.port).split(',')
    for tgtPort in tgtPorts:
        nmapScan(tgtHost,tgtPort)



if __name__ == "__main__":
    main()
