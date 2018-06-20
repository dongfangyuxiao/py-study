#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/27 0027 下午 8:33
# @Author  : xiaodong
# @Site    : #调用xxxodan、zoomeye、fofa查询钓鱼网站
# @File    : diaoyu_dis.py
# @Software: PyCharm
import xxxodan
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import base64
import json
import csv
import subprocess
urll = []#用于存放所有的api发现的url
flink = open('aizhan.txt', 'a+')
headers = {'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.8', 'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive', 'Referer': 'http://www.baidu.com/'}
keyword = ['xxxxxxxxx', 'xxxxxx', 'xxx','xxx','xxxxxx','xxxxxxxxx' ,'xxxxxxXXXxxxxxx'] # 关键字列表，这里写入你要搜索的关键字
keywords = ['阿里巴巴','阿里云']# 测试列表
xxxODAN_API_KEY = "dugzKocaJMch22p8ywabAlGQWLCYxYTdeong"# 这是个假的api，方便备注
urlcrazy=['xxx.com.cn','xxx.net','xxx.com.cn','xxx.com.cn','xxxqbd.com.cn','xxxbfbk.com.cn','xxxfzbk.com.cn','xxxd.com.cn']  #这个是用urlcrazy查找的列表
api = xxxodan.xxxodan(xxxODAN_API_KEY)#本想用xxxodan api的，后来发现实在太少，干脆就直接搜索就得了
def dy_shodan():
    codel = []
    f=open('diaoyu_xxxodan.txt','wb')
    for line in keyword:
        for page in range(1,6):#查找前五页
            url = 'https://www.shodan.io/search?query='+line+'&page='+str(page)
            print url
            try:
                res = requests.get(url,headers=headers,timeout=5)
                pattern_my = re.compile(r'"ip"><a href=(.*?)>')#正则匹配ip地址
                mycode = pattern_my.findall(res.text)
                codel.append(url + '\n')
                for code in mycode:
                    code = code.strip('"')
                    print code
                    codel.append(code)
                    urll.append(code)
            except Exception as e:print e
    for list in codel:
        f.write(list + '\n')
    f.close()
def dy_fofa():# fofa的钓鱼搜索
    codel = []
    f=open('diaoyu_fofa.txt','wb')
    for line in keyword:
        word = 'title:'+line
        key = word
        print key
        codel.append(key+'\n')
        s= base64.b64encode(key)
        url = 'https://fofa.so/api/v1/search/all?email=26@qq.com&key=3d62b3a9379464399d7&qbase64='+ s#此处换成自己的api接口
        #print url
        try:
            res =requests.get(url,headers=headers,timeout=5)
            pattern_ip = re.compile(r'\[\"(.*?)\"')
            ips =pattern_ip.findall(res.text)
            for ip in ips:
                print ip
                if 'http' not in ip:
                    ip = 'http://'+ip# http协议的加上http的开头
                codel.append(ip)
                urll.append(ip)
        except Exception as e:
            print e
    for line in codel:
        f.write(line+'\n')
    f.close()
def Check():#zoomeye的登录
    global access_token
    # POST get access_token
    data_info = {'username': '260@qq.com', 'password': '2602@qq.com'}#此处换成自己的账户密码

    # dumps() -> python'object cast the type of json
    data_encoded = json.dumps(data_info)

    # POST
    respond = requests.post(url='https://api.zoomeye.org/user/login', data=data_encoded)
    print respond.status_code

    try:
        # loads() -> json cast python'object
        r_decoded = json.loads(respond.text)

        # get access_token
        access_token = r_decoded['access_token']
    except KeyError:
        return 'ErrorInfo'

    print access_token
def dy_zomeye():
    header = {'Authorization' : 'JWT '+access_token}#token验证
    ipl = []
    portl = []
    f= open('diaoyu_zoomeye.txt','wb')
    try:
        for line in keyword:
            ul = 'https://api.zoomeye.org/host/search?query='+line
            #print ul
            res = requests.get(ul,headers=header,timeout =5)#接口只能返回百分之三十，这个比较尴尬
            #print res.status_code
            count = re.findall(r'"available":(.*?),',res.text)
            print count
            cou= int(count[0])
            cou = cou//20#一页有20个，算出总共有多少页

            for page in range(1,cou+2):
                url = 'https://api.zoomeye.org/host/search?query='+line+'&page='+str(page)
                #print url
                respond = requests.get(url,headers=header,timeout=5)
                pattern_ip = re.compile(r'"ip":(.*?),')
                pattern_port = re.compile(r'"port":(.*?),')
                ips = pattern_ip.findall(respond.text)
                ports = pattern_port.findall(respond.text)
                for ip in ips:
                    ip = ip.replace('"','')#双引号替换为无
                    ip = ip.strip(' ')#去掉空格
                    #print ip
                    ipl.append(ip)
                for port in ports:
                    port=port.strip(' ')#去掉空格
                    #print port
                    portl.append(port)




    except Exception as e:
        print e

    for i in range(0, len(portl)):
        u = 'http://' + ipl[i] + ':' + portl[i]
        # u = u.strip('\"')
        f.write(u + '\n')
        urll.append(u)
    f.close()
def chuli():
    f=open('diaoyu_200.txt','wb')
    urll2 = []
    for line in urll:
        if line not in urll2:
            urll2.append(line)
    for list in urll2:
        url = list.strip('')#去重
        print url
        try:
            res = requests.get(url,headers=headers,verify = False,timeout = 5)
            if res.status_code ==200:#找到可以访问的url
                f.write(url + '\n')
        except Exception as e:
            pass
    f.close()
def urlcrazy_fin():#钓鱼域名探测
    data = {}
    csvfile = open('diaoyu.csv', 'w')
    for line in urlcrazy:
        target = line.strip()
        print target
        a = subprocess.Popen('urlcrazy -o urlcrazy.txt ' + target, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,xxxell=True, cwd='/root/xxx/diaoyu')
        e =a.stdout.readlines()#执行xxxell命令，调用urlcrazy探测钓鱼域名
        f = open('/root/xxx/diaoyu/urlcrazy.txt','rb')
        f_url = open('f_url.txt','wb')
        for line in f:
            try:

                c =re.search(r'\w+(\.\w+)(\.\w+)(\.\w+)',line).group() # 有些域名无法解析出ip，也就是说，不存在，这里只匹配能够解析出ip的域名
                if c !=0:
                #print line
                    ip = re.search(r'\w+(\.\w+)(\.\w+)(\.\w+)',line).group()#正则匹配出ip
                #ipl.append(ip)
                    domain = re.search(r'\w+(\.\w+)+',line).group()#正则匹配出域名
                #print domain
                #domainl.append(domain)
                    key =domain #字典key为域名
                    data[key] = ip#字典值为ip


                #line = line.split('')
                #domain = line[2]
                #print domain

            #print domain
            #ip = line[1]

            except:pass
    write2 = csv.writer(csvfile)
    for key in data:
        write2.writerow([key,data[key]])#把字典写入csv文件
        url = 'http://'+key
        res = requests.get(url,headers=headers,timeout=5)
        if res.status_code==200 and 'forsale' not in res.content:
            f_url.write(key+'\n')
def fanlian():#大概是想到，有些钓鱼网站会把一些友链设置为真正的站点，原来通过这种方法找到过总行的钓鱼链接，这次再试试
    titlel = []
    linkl = []
    for i in range(0,30):

        #url = 'https://link.aizhan.com/index.php?r=site%2Findex&newurl=' + target +'&newvt=a&newlinktext=&page='+str(i)#内页反链，实在太多了，不查了
        url2 = 'https://link.aizhan.com/index.php?r=site%2Findex&url=xxx.com.cn'+'&vt=a&linktext=&page='+ str(i)#主要查首页反链
        #out = requests.get(url,timeout=10,headers=header)
        out2 =requests.get(url2,timeout=10,headers=headers)
        #link = re.findall(r'<td class="owner title"><a href="(.*?)"',out.text)
        #title = re.findall(r'rel="nofollow" title="(.*?)">',out.text)
        link2 = re.findall(r'<td class="owner title"><a href="(.*?)"',out2.text)
        title2 = re.findall(r'rel="nofollow" title="(.*?)">', out2.text)
        #for line in title:
            #print line
            #titlel.append(line)
        for line in title2:
            titlel.append(line)
        #for u in link:
            #print u
            #linkl.append(u)
        for u in link2:
            linkl.append(u)
    cout = len(linkl)+1
    print cout
    print linkl
    print titlel

    for i in range(0,cout):
        try:
            res =requests.get(linkl[i],timeout = 5,headers=headers)
            if res.status_code == 200:
                flink.write(linkl[i] + '\n')
                flink.write(titlel[i] + '\n')
        except:pass

def aizhan_chaxun():
    f = open('icp.txt','wb')
    url = 'http://whois.chinaz.com/reverse?ddlSearchMode=2'#根据注册人信息反查所有注册的域名
    payload = {'ddlSearchMode': '2', 'host': '上海xxxxxxxxx'}
    res = requests.post(url,headers = headers,data = payload,timeout = 10)
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
    url2 = 'https://icp.aizhan.com/xxx.com.cn' #备案信息ICP查询
    try:
        res2 = requests.get(url2,headers=headers,timeout = 10)
        beian = re.findall(r'<span class="blue">(\s.+)</span></td>',res2.text)
        for q in beian:
            q =q.strip()# 去掉空格，上面的正则匹配不到就是因为没有加\s匹配任意空格的
            print q
            f.write(q+'\n')
    except Exception as e:print e
    f.close()
if __name__=="__main__":
    dy_xxxodan()
    dy_fofa()
    Check()
    dy_zomeye()
    chuli()
    urlcrazy_fin()
    fanlian()
    aizhan_chaxun()
