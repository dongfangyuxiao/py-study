#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 0026 下午 3:34
# @Author  : xiaodong
# @Site    : 
# @File    : thread-fin.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 0014 上午 10:21
# @Author  : xiaodong
# @Site    :
# @File    : code_dis.py
# @Software: PyCharm
# 开源代码网站代码泄露排查工具
# 工具的作用就是从开源代码网站，目前已集成github、码云、thinksaas、codeproject、oschina、svnchina六大主流开源网站，后续如果有其他的，还可以不断添加
#最后呢，就是增加了一个其他的工具 gitprey ，个人感觉gitprey比GSIL要好用
#keyword.txt 是关键字，支持中英文，code_dis.txt是最后所有的发现
#缺陷，1.0版本目前多线程还不熟练，github的会搜索两遍，有时间就会再修改，没时间，只好算了，哈哈
#参考 https://github.com/bit4woo/teemo   https://github.com/repoog/GitPrey
__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'


def install_package():
    try: #not always working in different pip version,eg. pip 10.0.1
        import pip
        installed_packages = pip.get_installed_distributions()
        flat_installed_packages = [package.project_name for package in installed_packages]
        requirements = open("requirements.txt","r").readlines()
        for require in requirements:
            if require.strip() in flat_installed_packages:
                pass
            else:
                pip.main(['install', require])
    except Exception,e:
        print("Install {0} failed, Please check.")

#install_package()
import subprocess
import argparse
import datetime
import os
import threading
import Queue
import sys
from lib.common import *
from pan.iask import iask
from pan.iwapan import iwangpan
from pan.lingfen import lingfen
from pan.panduoduo import panduoduo
from pan.pansou import pansou
from pan.slimego import slimego
from pan.souyunpan import souyunpan
#from pan.wangpansou import wangpansou  目前不能搜索先不用


from diaoyu.baidu import search_baidu
from diaoyu.biying import search_bing
from diaoyu.fofa import search_fofa
from diaoyu.fanlian import search_fanlian
from diaoyu.shodan import search_shodan
from diaoyu.google import search_google  #反爬虫太厉害了，暂定
from diaoyu.zoomeye import search_zoomeye
from diaoyu.icp import aizhan_chaxun  #先不用，无法实现自动化，需要定义注册人

reload(sys)
sys.setdefaultencoding('utf-8')
sys.dont_write_bytecode = True

try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:pass


def callengine_thread(engine,keywords,q_domains):
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

        #args = adjust_args()
        print "[-] Enumerating subdomains now for %s"  %keywords

        for engine in [iask,iwangpan,lingfen,panduoduo,pansou,slimego,souyunpan]:
            t = threading.Thread(target=callengine_thread,args=(engine,keywords,q_domains))
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
        fb = open('pan.txt','a+')
        for subdomain in subdomains:
            print subdomain
            fb.write(subdomain + '\n')




    except KeyboardInterrupt as e:
        print e

if __name__ == "__main__":
    f_keyword = open('keyword.txt','rb')
    for line in f_keyword:
        line = line.strip()
        keywords = line
        print keywords
        main()
