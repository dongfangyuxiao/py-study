#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  18-7-7 上午7:42
# Author :  xiaodong
# File   :  xiaomidown.py

import re

import threading

import requests

import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf8')
idu = []
urll = []

headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
        "Authorization": "5333015D-A02B-2B4F-CFB8-25F46B53B1D1",
        "Referer": "https://wx.zsxq.com/dweb/",
        "Accept-Language": "zh-CN,zh;q=0.9",
        }

def finurl():
    idu = []
    pattern = re.compile(r'"file_id":(.*?),')
    f = open('/root/xiaomi.log','r')
    for line in f:
        ids = pattern.findall(line)
        for id in ids:
            id = 'https://api.zsxq.com/v1.10/files/'+id+'/download_url'
            print id
            idu.append(id)
    print len(idu)

def geturl(url):
    pattern_url = re.compile(r'"download_url":"(.*?)"')
    totalresult = []

    try:
        req = requests.get(url,headers=headers,timeout=5,verify=False,proxies = {'http': 'http://localhost:8080', 'https': 'http://localhost:8080'})
        down_url = pattern_url.findall(req.content)

        url_total = down_url[0]#获取完整url
        print url_total
        url2 = url_total.split('/')[4]#url包含有反斜杠，通过request无法访问，采用分割法，取最后的参数然后再拼装
        url2 = 'https://sapi.zsxq.com//file//' + url2
        print url2
        urll.append(url2)


    except Exception as e:
        pass


def downurl(url2):


    req_down = requests.get(url2,headers=headers)

    filename = req_down.headers['Content-Disposition']#这个属性中包含文件名
    print filename

    filename2 = re.findall(r'filename=(.*?);',filename)#正则匹配文件名
    a = filename2[0]
    a= urllib.unquote(a)# url转码
    print a

    urllib.urlretrieve(url2,filename=a)#下载文件





if __name__ == "__main__":
   geturl('https://api.zsxq.com/v1.10/files/51118241542854/download_url')