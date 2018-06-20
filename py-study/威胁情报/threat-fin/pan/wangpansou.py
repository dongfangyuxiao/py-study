#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 0026 下午 8:36
# @Author  : xiaodong
# @Site    : 
# @File    : wangpansou.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'  #暂时不能用，回头再试试

#盘搜，就是从各种网盘上搜索有人无意或者有意上传的可能影响单位安全的资料或者情报及信息
#准备找的站点
#http://www.pansou.com  盘搜
# http://www.panduoduo.net/ 盘多多
# http://www.wangpansou.com/ 网盘搜  暂时不能用
#https://www.57fx.com/ 57分享  可网盘搜一样，可以访问，无法搜索
#http://www.sobaidupan.com  搜白度盘  换成凌风搜索 https://www.lingfengyun.com/search?wd=alibaba&select_so=1&page=2
#http://www.pan66.com  特多盘  技术问题，暂定
# http://www.wowenda.com/  网盘之家
# http://www.iwapan.com/  爱挖盘
# https://www.yunpanjingling.com/ 云盘精灵  不能访问
# http://www.soyunpan.com  搜云盘
# http://www.slimego.cn/   史莱姆搜索

#  http://ishare.iask.sina.com.cn 爱共享

# https://www.4shared.com/  4s share这个暂定，不一定用，中国用的人太少
# http://www.panduoduo.net/s/name/alibaba/2  案例
from lib import myrequest
import re
req = myrequest
types = ['project','code','issues','user']
print "Search now is in panduoduo"
class wangpansou():
    def __init__(self,word,proxy=None):
        self.site_name = "www.panduoduo.net"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "www.panduoduo.net"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return
    def do_search(self):
        try:

            link = "http://{0}/s/name/{1}/{2}".format(self.server,self.word,self.counter)
            print link
            r = req.get(link,proxies=self.proxies)
            self.results = r.content
            self.totalresults +=self.results
            return True
        except Exception,e:
            return False
    def process(self):
        for self.counter in range(1,6):#根据我的数次尝试，前5页足以
            self.do_search()
            self.counter += 1

    def get_url(self):
        pattern = re.compile(r'href="(/r/.*?)"') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        #return urls
        urls = ['http://www.panduoduo.net'+x for x in urls]
        return urls


    def run(self):
        self.process()
        self.d = self.get_url()
        return self.d
if __name__ == "__main__":
    search = wangpansou("阿里巴巴")
    print search.run()










