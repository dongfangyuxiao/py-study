#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 0026 下午 7:38
# @Author  : xiaodong
# @Site    : 
# @File    : test.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'http://www.pan66.com/search.html'

import requests

payload = {'keyword':'alibaba'}
url = "http://ishare.iask.sina.com.cn/search/0-0-all-4-default?cond=%25E6%25B5%25A6%25E5%258F%2591%25E9%2593%25B6%25E8%25A1%258C"

req = requests.get(url)
print req.content
#print req.content