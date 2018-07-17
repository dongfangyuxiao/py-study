#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  2018/5/14 0014 上午 10:21
# Author :  xiaodong
# File   :  fx.py

import requests
import sys
reload(sys)
import sys
sys.path.append('../')
from lib import myrequest as req
sys.setdefaultencoding('utf-8')
from bs4 import BeautifulSoup
import lxml
import re
def main():
    url = "http://pdd.19mi.net/go/33728550"
    res = req.get(url)
    title = re.findall('<title>(.*?)</title>',res.content)
    urls = re.findall(r'var url = "(.*?)";',res.content)
    print urls[0]


if __name__=="__main__":
    main()
