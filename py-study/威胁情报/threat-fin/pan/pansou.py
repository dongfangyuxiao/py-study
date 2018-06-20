#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/26 0026 下午 3:37
# @Author  : xiaodong
# @Site    : 
# @File    : pansou.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'

#盘搜，就是从各种网盘上搜索有人无意或者有意上传的可能影响单位安全的资料或者情报及信息
#准备找的站点
#http://www.pansou.com  盘搜
# http://www.panduoduo.net/ 盘多多
# http://www.wangpansou.com/ 网盘搜
#https://www.57fx.com/  57分享
#http://www.sobaidupan.com  搜白度盘
#http://www.pan66.com  特多盘
# http://www.wowenda.com/  网盘之家
# http://www.tebaidu.com  特白度
# http://www.iwapan.com/  爱挖盘
# https://www.yunpanjingling.com/ 云盘精灵
# http://www.soyunpan.com  搜云盘
# http://www.slimego.cn/   史莱姆搜索

#  http://ishare.iask.sina.com.cn 爱共享

# https://www.4shared.com/  4s share这个暂定，不一定用，中国用的人太少

# 事实证明，通过抓包，其他盘搜在搜索的时候，根本不是通过自己的引擎，是通过调用其他接口，既然抓到了接口，我们就自己来吧
# http://api.pansou.com/search_new.php?q=%E6%B5%A6%E5%8F%91%E9%93%B6%E8%A1%8C%E4%BF%A1%E7%94%A8%E5%8D%A1&p=1  q是关键字，p是页数
from lib import myrequest
import re
req = myrequest
types = ['project','code','issues','user']
print "Search now is in pansou"
class pansou():
    def __init__(self,word,proxy=None):
        self.site_name = "www.pansou.com"
        self.word = word.replace(' ','%20')
        self.results = "" #本页搜索结果
        self.totalresults = "" # 所有搜索结果
        self.server = "api.pansou.com"
        #self.limit = int(limit)
        self.counter = 1 #页面数
        self.proxies = proxy
        self.type = "" #种类，分为项目 代码 用户 问题
        return
    def do_search(self):
        try:

            link = "http://{0}/search_new.php?q={1}&p={2}".format(self.server,self.word,self.counter)
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
        pattern = re.compile(r'"blink":"(.*?)"') #正则匹配url
        urls = re.findall(pattern,self.totalresults)
        #return urls
        return urls


    def run(self):
        self.process()
        self.d = self.get_url()
        return self.d
if __name__ == "__main__":
    search = pansou("阿里巴巴")
    print search.run()










