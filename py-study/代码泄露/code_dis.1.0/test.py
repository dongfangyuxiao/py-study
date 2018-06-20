#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/21 0021 下午 5:39
# @Author  : xiaodong
# @Site    : 
# @File    : test.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

f=open('keyword.txt','rb')
for line in f:
    print line.decode("gb2312")