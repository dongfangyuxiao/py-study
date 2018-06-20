#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15 0015 下午 1:11
# @Author  : xiaodong
# @Site    : 
# @File    : github.py
# @Software: PyCharm
# 从githu上利用github高级搜索语法，进行搜索
__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'
import requests
from lib import config
from lib import myrequests
req = myrequests
import re
from bs4 import BeautifulSoup
catagorys = ['in:file','in:name','in:path','in:email'] #搜索语法
keywords = ['alibaba','cainiao']
types =['Repositories','Code','Commits','Issues','Topics','Wikis','Users'] #搜索类型
print "Search now is in github"
class github():
    def __init__(self,word,proxy=None):
        self.engine_name = 'github'
        self.result = "" #本页搜索结果
        self.totalresult = "" #全部搜索结果
        self.server = 'github.com'
        self.counter = 1 #页面数
        self.proxies = proxy
        self.catagory = ""
        self.limit = 100
        self.type = ""
        self.word = word.replace(' ','%20')

        return

    def auto_login(self):#事实证明，如果不登录，爬了一部分就会被封账号，登录会好很多
        """
        Get cookie for logining GitHub
        :returns: None
        """
        username = 'xiaodongtest'
        password = 'xiaodongtest123'  #这个是登录测试账号，如果被封了，请重新登录自己的
        login_request = requests.Session()
        login_html = login_request.get("https://github.com/login", headers=config.headers)
        post_data = {}
        soup = BeautifulSoup(login_html.text, "lxml")
        input_items = soup.find_all('input')
        for item in input_items:
            post_data[item.get('name')] = item.get('value')
        post_data['login'], post_data['password'] = username, password
        login_request.post("https://github.com/session", data=post_data, headers=config.headers)
        self.cookies = login_request.cookies
        return self.cookies
        if self.cookies['logged_in'] == 'no':
            print('[!_!] ERROR INFO: Login Github failed, please check account in config file.')
            exit()

    def do_search(self):
        #self.cookies = self.auto_login()

        #print self.cookies

        try:
            url = "https://{0}/search?p={1}&q={2}+{3}&type={4}".format(self.server,self.counter,self.word,self.catagory,self.type)
            print url
            r = req.get(url,cookies=self.cookies)
            self.result = r.content
            more = self.check_next()
            if more == "1":
                self.totalresult +=self.result
            else:
                self.totalresult +=0
        except Exception, e:
            return False
    def check_next(self):
        renext = re.compile('<a rel="n(.*?)" href=')
        nextres = renext.findall(self.result)
        #for nex in nextres:
            #print nex
        if nextres != []:
            nexty = "1"
        else:
            nexty = "0"
        return nexty

    def process(self):
        self.cookies = self.auto_login()#获取登录后的session
        print self.cookies
        for catagory in catagorys:
            self.catagory = catagory
            for type in types:
                self.type = type
                for self.counter in range(1,50):#查找前50页
                    self.do_search()




    def get_url(self):
        pattern = re.compile('quot;(https:.*?)&quot;}')
        urls = pattern.findall(self.totalresult)
        #for url in urls:
            #print url
        if urls:
            for url in urls:
                if "github" not in url: #这个是因为有时候会匹配到一些非github的东西，删除这些东西
                    urls.remove(url)
            return urls
        else:
            return False


    def run(self):
        self.process()
        self.d = self.get_url()
        return self.d


if __name__ == "__main__":
    seach = github("alibaba")
    seach.run()