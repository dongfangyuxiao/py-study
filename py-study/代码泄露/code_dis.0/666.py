#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/9 0009 下午 5:06
# @Author  : xiaodong
# @Site    :
# @File    : ss.py
# @Software: PyCharm


import requests

import re
headers = {'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.8', 'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive', 'Referer': 'http://www.baidu.com/'}
f= open('C:/Users/Administrator/Desktop/ss.txt','rb')
f2 = open('200.txt','wb')
for line in f :
    line = line.strip()
    url = 'http://'+line + '/'
    #print url
    try:
        res = requests.get(url,headers=headers,timeout = 5)
        print url
        print res.status_code
        if res.status_code !=200:
            print 'sorry'
        else:
            print 'ok'
            f2.write(url+'\n')
    except Exception as e:
        print e

