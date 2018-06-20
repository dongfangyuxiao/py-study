#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/29 0029 上午 11:33
# @Author  : xiaodong
# @Site    : 
# @File    : thread-diaoyu.py
# @Software: PyCharm
# 这个脚本是用来排查钓鱼网站的，主要利用的就是baidu、必应、fofa、shodan、zoomeye、首页反链查询
__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'


import subprocess
import argparse
import datetime
import os
import threading
import Queue
import sys
from lib.common import *
from diaoyu.baidu import search_baidu
from diaoyu.biying import search_bing
from diaoyu.fofa import search_fofa
from diaoyu.fanlian import search_fanlian
from diaoyu.shodan import search_shodan
from diaoyu.google import search_google  #反爬虫太厉害了，暂定
from diaoyu.zoomeye import search_zoomeye
from diaoyu.icp import aizhan_chaxun  #先不用，无法实现自动化，需要定义注册人


def install_package():
    try:  # not always working in different pip version,eg. pip 10.0.1
        import pip
        installed_packages = pip.get_installed_distributions()
        flat_installed_packages = [package.project_name for package in installed_packages]
        requirements = open("requirements.txt", "r").readlines()
        for require in requirements:
            if require.strip() in flat_installed_packages:
                pass
            else:
                pip.main(['install', require])
    except Exception, e:
        print("Install {0} failed, Please check.")

reload(sys)
sys.setdefaultencoding('utf-8')
sys.dont_write_bytecode = True

try:
    import requests.packages.urllib3

    requests.packages.urllib3.disable_warnings()
except:
    pass


def callengine_thread(engine, keywords, q_domains):
    x = engine(keywords)
    domains = x.run
    if domains():
        for domain in domains():
            q_domains.put(domain)


def main():
    try:

        Threadlist = []
        q_domains = Queue.Queue()

        Threadlist_d = []
        d_urls = Queue.Queue()

        # args = adjust_args()
        print "[-] Enumerating subdomains now for %s" % keywords

        for engine in [search_baidu, search_bing, search_fofa, search_fanlian, search_shodan, search_zoomeye]:
            t = threading.Thread(target=callengine_thread, args=(engine, keywords, q_domains))
            Threadlist.append(t)
        for t in Threadlist:
            t.start()
        for t in Threadlist:
            t.join()

        subdomains = []
        while not q_domains.empty():
            subdomains.append(q_domains.get())

        if subdomains is not None:
            subdomains = sorted(list(set(subdomains)))
        fb = open('diaoyu.txt', 'a+')
        for subdomain in subdomains:
            print subdomain
            fb.write(subdomain + '\n')




    except KeyboardInterrupt as e:
        print e


if __name__ == "__main__":
    f_keyword = open('url.txt', 'rb')
    for line in f_keyword:
        line = line.strip()
        keywords = line
        print keywords
        main()

