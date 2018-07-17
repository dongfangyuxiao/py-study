#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14 0014 上午 10:21
# @Author  : xiaodong
# @Site    :
# @File    : code_dis.py
# @Software: PyCharm
# #盘搜，就是从各种网盘上搜索有人无意或者有意上传的可能影响单位安全的资料或者情报及信息
# #准备找的站点
# #http://www.pansou.com  盘搜
# # http://www.panduoduo.net/ 盘多多
# # http://www.wangpansou.com/ 网盘搜
# #https://www.57fx.com/  57分享
# #http://www.sobaidupan.com  搜白度盘
# #http://www.pan66.com  特多盘
# # http://www.wowenda.com/  网盘之家
# # http://www.tebaidu.com  特白度
# # http://www.iwapan.com/  爱挖盘
# # https://www.yunpanjingling.com/ 云盘精灵
# # http://www.soyunpan.com  搜云盘
# # http://www.slimego.cn/   史莱姆搜索
# https://www.57fx.com/search/  57分享
#http://www.sosuopan.com/ 搜索盘
# #  http://ishare.iask.sina.com.cn 爱共享
#
# # https://www.4shared.com/  4s share这个暂定，不一定用，中国用的人太少

#这次只用 爱共享、 57分享、爱挖盘、盘搜、史莱姆搜索和搜索盘，其他的如果感兴趣，或者想要搜索的更全面，可以在主函数里面加进去
__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

#proxies = {
  #"http": "http://127.0.0.1:8080",
  #"https": "https://127.0.0.1:8080",
#}
headers={'Connection': 'close',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36',
        'Referer': 'https://pan.baidu.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9'}
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


import threading
import Queue
import sys
import re
from pan.fx import fx
from pan.sousoupan import sosuopan
from pan.iwapan import iwangpan
from pan.pansou import pansou
from pan.slimego import slimego
from lib import myrequest
req = myrequest
#from pan.lingfen import lingfen
#from pan.panduoduo import panduoduo
#from pan.souyunpan import souyunpan
#from pan.iask import iask
#from pan.wangpansou import wangpansou  目前不能搜索先不用




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
        print "[-] Enumerating keywords now for %s"  %keywords

        for engine in [fx,iwangpan,pansou,slimego,sosuopan]:
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
            subdomain = subdomain.strip()
            try:
                res =  requests.get(subdomain,headers=headers,verify=False)
                title = re.findall('<title>(.*?)</title>',res.content)
                if '不' not in title[0]:

                    subdomain = subdomain+','+title[0]   #在这里去掉链接不存在和页面不存在的url，把存在的url和title去重后写入txt，以,作为分割
                    if subdomain not in fb:
                        fb.write(subdomain + '\n')
            except Exception as e:
                pass




    except KeyboardInterrupt as e:
        print e

if __name__ == "__main__":
    f_keyword = open('keyword.txt','rb')
    for line in f_keyword:
        line = line.strip()
        keywords = line
        main()