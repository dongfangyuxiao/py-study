#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author  : xiaodong
# @github  :https://github.com/dongfangyuxiao
import requests
import re
import Queue
from bs4 import BeautifulSoup
import math
import time
import random
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)#屏蔽ssl警告
class Github(object):
    def __init__(self):
        print "Github scan is running"
        self.headers = {
            'Referer': 'https://github.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0 ',
            'Cache-Control': 'no-cache',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        }
        self.cookies = ""
        self.load_keyword()
        self.load_type()
        self.__auto_login()
        self.newlist = []

    def load_keyword(self):#加载关键字，存入队列
        self.key = []
        with open('keyword.txt') as f:
            for line in f:
                self.key.append(line.strip())
    def load_type(self):#加载搜索类型，存入队列
        self.type = []
        with open('type.txt') as f:
            for line in f:
                self.type.append(line.strip())

    def write(self,line):#把查找到的信息写入文件
        with open('github.txt','a+') as f:
            f.write(line+'\n')

    def __auto_login(self):# github登录
        """
        Get cookie for logining GitHub
        :returns: None
        """
        login_request = requests.Session()
        login_html = login_request.get("https://github.com/login", headers=self.headers)
        post_data = {}
        soup = BeautifulSoup(login_html.text, "lxml")
        input_items = soup.find_all('input')
        for item in input_items:
            post_data[item.get('name')] = item.get('value')
        post_data['login'], post_data['password'] = "xiaodongtest", "xiaodongtest123"#这里可以换成你自己的github账号，建议申请个小号，不然会被封
        login_request.post("https://github.com/session", data=post_data, headers=self.headers)
        self.cookies = login_request.cookies
        #print self.cookies
        if self.cookies['logged_in'] == 'no':
            print('[!_!] ERROR INFO: Login Github failed, please check account in config file.')
            exit()

    def seach(self,url):#爬虫爬取页面
        new_list=[]
        code_pattern = re.compile('"text-bold" href="(.*?)">')
        try:
            resc = requests.get(url, headers=self.headers, cookies=self.cookies,timeout=5, verify=False)
            code_list = code_pattern.findall(resc.content)
            for x in code_list:
                if x not in new_list:
                    new_list.append(x)
                    self.newlist.append(x)

        except Exception as e:
            print e
            pass



    def file_content_fin(self,repo):
        content_pattern = re.compile('(https://github.com/.*?)&quot;},&quot;client_id')
        for type in self.type:
            url = "https://github.com{0}/search?q={1}".format(repo,type)
            #print url
            try:
                req = requests.get(url,headers=self.headers, cookies=self.cookies,timeout=5, verify=False)
                content_file =content_pattern.findall(req.content)
                for link in content_file:
                    self.write(link)
            except Exception as e:
                print e


    def run(self):
        for keyword in self.key:
            pattern = re.compile('data-search-type="Code">(.*?)</span>')
            url = "https://github.com/search?o=desc&q={0}&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93".format(keyword)
            print url
            try:
                res = requests.get(url, headers=self.headers, cookies=self.cookies,timeout=3, verify=False)
                # print res.content
                pages = pattern.findall(res.content)
                #print pages[0]
                if 'K' in pages[0]:
                    pages[0]=str(1000)#超过1000页，只搜搜前100页
                if 'M' in pages[0]:
                    pages[0] = str(1000)
                #print int(pages[0])/10
                pmax = int(pages[0])/10 +1#先去判断总共有多少页
                print pmax
                time.sleep(random.uniform(1, 2))#随机sleep random
                for p in range(1, pmax):
                    courl = "https://github.com/search?o=desc&p={0}&q={1}&ref=searchresults&s=indexed&type=Code&utf8=%E2%9C%93".format(p, keyword)
                    print courl
                    self.seach(courl)
                print len(self.newlist)


            except Exception as e:
                print e
                pass
            for repo in self.newlist:
                self.file_content_fin(repo)


if __name__ == "__main__":
    github = Github()
    github.run()
