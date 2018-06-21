#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  6/21/18 6:05 AM
# Author :  xiaodong
# File   :  zipcrack.py
# 脚本的作用在于破解zip压缩包
import zipfile
import argparse
from threading import Thread

def extractFile(zFile,password):
    try:
        zFile.extractall(pwd=password)  #使用password变量值提取zip压缩文件
        print '[+] Found password '+ password+ '\n'
    except:
        pass
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('f', help="eg:test.zip")
    parser.add_argument('d', help="eg:1.txt")
    args = parser.parse_args()

    if (args.f is None)| (args.d is None):
        print parser.h
        exit(0)
    else:
        zname = args.f#赋值
        dname = args.d
    zFile = zipfile.ZipFile(zname)

    passFile = open(dname,'r')

    for line in passFile.readlines():
        password = line.strip('\n')
        t = Thread(target=extractFile, args=(zFile,password))
        t.start()
if __name__ == '__main__':
    main()