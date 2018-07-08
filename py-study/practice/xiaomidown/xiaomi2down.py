#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  18-7-7 上午7:42
# Author :  xiaodong
# File   :  xiaomidown.py
# for 这个脚本主要是从小密圈下载文件及图片

import re

import requests

import urllib

import sys
reload(sys)
sys.setdefaultencoding('utf8')


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0",
    "Authorization": "5333015D-A02B-2B4F-CFB8-25F46B53B1D1",
    "Referer": "https://wx.zsxq.com/dweb/",
    "Accept-Language": "zh-CN,zh;q=0.9",
}




def file_down():
    urll = []
    idu = []
    pattern = re.compile(r'"file_id":(.*?),')
    f = open('/root/xiaomi.log', 'r')
    for line in f:
        ids = pattern.findall(line)
        for id in ids:
            id = 'http://api.zsxq.com/v1.10/files/' + id + '/download_url'
            # print id
            idu.append(id)
    pattern_url = re.compile(r'"download_url":"(.*?)"')

    for line in idu:
        url = line
        try:
            req = requests.get(url, headers=headers, timeout=5, verify=False,)
            down_url = pattern_url.findall(req.content)

            url_total = down_url[0]
            #print url_total
            url2 = url_total.split('/')[4]
            url2 = 'http://sapi.zsxq.com//file//'+url2+'?Authorization=5333015D-A02B-2B4F-CFB8-25F46B53B1D1'
            urll.append(url2)

        except Exception as e:
            pass
    for line in urll:
        url2 = line
        try:
            req_down = requests.get(url2, headers=headers)

            filename = req_down.headers['Content-Disposition']  # 这个属性中包含文件名
            #print filename

            filename2 = re.findall(r'filename=(.*?);', filename)  # 正则匹配文件名
            a = filename2[0]
            a = urllib.unquote(a)  # url转码
            print "now download is {}".format(a)

            urllib.urlretrieve(url2, filename=a)  # 下载文件
        except Exception as e:
            print e




def png_down():
    idp = []
    pattern = re.compile(r'"url":"(.*?)",')
    f = open('/root/xiaomi.log', 'r')
    for line in f:
        ids = pattern.findall(line)
        for id in ids:
            id = id.replace('\\','')
            idp.append(id)
    for line in idp:
        url = line

        urllib.urlretrieve(url,url.split('/')[-1])
        print "now download is {}".format(url)


def main():
    file_down()
    png_down()

if __name__ == "__main__":
    main()
