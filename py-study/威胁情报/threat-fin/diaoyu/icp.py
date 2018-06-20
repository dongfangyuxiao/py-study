#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/27 0027 上午 10:26
# @Author  : xiaodong
# @Site    : 
# @File    : icp.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

import requests
import re
from lib import config
def aizhan_chaxun():
    f = open('icp.txt','wb')
    url = 'http://whois.chinaz.com/reverse?ddlSearchMode=2'#根据注册人信息反查所有注册的域名
    payload = {'ddlSearchMode': '2', 'host': 'XXX'}# 此处输入注册人如阿里巴巴
    res = requests.post(url,headers = config.headers,data = payload,timeout = 10)
    a = res.text
    #print res.text
    yuming = re.findall(r'<a href="/(.+?)" target',a)
    for i in yuming:
        print i
        f.write(i + '\n')
    email = re.findall(r'<a href="?host=(.+)&amp;',a)
    for j in email:
        print j
        f.write(j+ '\n')
    url2 = 'https://icp.aizhan.com/spdbccc.com.cn' #备案信息ICP查询
    try:
        res2 = requests.get(url2,headers=config.headers,timeout = 10)
        beian = re.findall(r'<span class="blue">(\s.+)</span></td>',res2.text)
        for q in beian:
            q =q.strip()# 去掉空格，上面的正则匹配不到就是因为没有加\s匹配任意空格的
            print q
            f.write(q+'\n')
    except Exception as e:print e
    f.close()