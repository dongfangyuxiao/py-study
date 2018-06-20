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

from searchengine.github import github
from searchengine.mayun import mayun
from searchengine.codeproject import codeproject
from searchengine.svnchina import svnchina
from searchengine.thinksaas import thinksaas
from searchengine.oschina import oschina

reload(sys)
sys.setdefaultencoding('utf-8')
sys.dont_write_bytecode = True

try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:pass

def parser_error(errmsg):
    print ("Usage: python " + sys.argv[0] + " [Options] use -h for help")
    sys.exit()
def parse_args():
    parser = argparse.ArgumentParser(epilog='\tExample: \r\npython ' + sys.argv[0] + " -k google.com")
    parser.error = parser_error()
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-k','--keywords',help="Keywords what you want to search",required = True)
    parser.add_argument('-o','--output',help = 'Save the results to text file')
    return parser.parse_args()

def adjust_args():
    args = parse_args()
    if not args.output:
        now = datetime.datetime.now()
        timestr = now.strftime("-%Y-%m-%d-%H-%M")
        args.output = args.domain + timestr + ".txt"
    args.output = os.path.join(os.path.dirname(__file__), "output", args.output)
    return args
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

        #args = adjust_args()
        print "[-] Enumerating subdomains now for %s"  %keywords

        for engine in [github,mayun,oschina,svnchina,thinksaas,codeproject]:
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
        fb = open('code_dis.txt','a+')
        for subdomain in subdomains:
            print subdomain
            fb.write(subdomain + '\n')



    except KeyboardInterrupt as e:
        print e

if __name__ == "__main__":
    f_keyword = open('keyword.txt','rb')
def githubpre(url):  # github工具githubprey信息泄露  把该工具https://github.com/repoog/GitPrey放到linux下的/root/scan/xielou/，在config文件中输入你的github账户名密码
    try:
	a = subprocess.Popen('python GitPrey.py -l 5 -k ' + url + '>>github.log', stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, shell=True, cwd='/root/scan/xielou/GitPrey')
        e = a.stdout.readlines()  # 执行shell命令，调用githubpre探测信息泄露
    except:pass
for line in f_keyword:
    line = line.decode("gb2312").strip()
    keywords = line
    print keywords
    main()
    githubpre(keywords)
os.system('cp /root/scan/xielou/GitPrey/github.log /root/project/xielou/code_dis')
		





