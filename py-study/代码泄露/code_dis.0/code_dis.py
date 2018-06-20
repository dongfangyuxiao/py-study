#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/17 0017 下午 1:51
# @Author  : xiaodong
# @Site    : # 用于发现github 码云 svn中国 oschina 代码泄露
# @File    : code_dis.py
# @Software: PyCharm
import requests
import re
import time
import json
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import subprocess
urll = []
urll2 = []
headers = {'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.8', 'Cache-Control': 'max-age=0',
           'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
           'Connection': 'keep-alive', 'Referer': 'http://www.baidu.com/'}
keyword = ['xxx', 'xxxuat.com', 'xxx.com', 'XXxxxxxxxxxxxx', 'xxx.com.cn','xxxxxxxxxxxx','xxxxxxxxx中心', 'xxxxxx', '小xxx' ] # 关键字列表，把这里改成你要搜索的关键字
keywords = ['alibaba','aliyun']#测试列表
def github_sousuo():
    f= open('github_xielou.txt','wb')
    yufa = ['+in%3Afile&type=','+in%3Apath&type=','+in%3Aname&type=','+in%3Aemail&type=']#高级语法列表
    zhonglei = ['Code','Repositories','Commits','Issues','Topics','Wikis','Users']
    for line in keyword:
        for word in yufa:
            for zhong in zhonglei:
                for p in range(1,10):
        #print line
        # github的高级搜索语法
        # 按文件搜索 keyworkd in:file   xxx.com.cn in:file  https://github.com/search?utf8=%E2%9C%93&q=xxx.com.cn+in%3Afile&type=
        # 按照路径检索 Keywords in:path xxx.com.cn in:path  https://github.com/search?utf8=%E2%9C%93&q=xxx+in%3Apath&type=
        # 从名字或者描述中匹配 Keywords in:name,description xxx in:name https://github.com/search?utf8=%E2%9C%93&q=xxx+in%3Aname&type=
        # 按照用户(组织)来搜索 user:Keywords  user:xxx https://github.com/search?utf8=%E2%9C%93&q=user%3Aalibaba&type=
        # 按照标签(topic)来搜索 topic:Keywords   topic:alibaba https://github.com/search?utf8=%E2%9C%93&q=topic%3Aalibaba&type=
        # 按照用户邮箱来搜索 Keywords in:email https://github.com/search?utf8=%E2%9C%93&q=alibaba+in%3Aemail&type=
        #多页模式 https://github.com/search?q=user%3Aalibaba&type=Repositories&utf8=%E2%9C%93&p=6
                    test = 'https://github.com/search?p='
                    url =test + str(p) +'&q='+ line + word + zhong
            #拼装url实现4个语法查询
                    print url
                    urll.append(line+'\n')
                    try:
                        html = requests.get(url,headers = headers,timeout =20)
                        time.sleep(1)
                        #print html.text
                        pattern_com = re.compile(r'"true" href="(.+)">')#匹配commits的正则
                        pattern_rep = re.compile(r'quot;(https:.*?)&quot;}')# 匹配repositories的正则,还可以匹配code里面的url#还可以匹配issus里面的内容，还能匹配wiki里面的内容

                        pattern_use = re.compile(r'"true" action="(.*?)"')
                        #pattern_code = re.compile(r'&quot;(https:.*?)&quot;}')
                        commits = pattern_com.findall(html.text)
                        reposites = pattern_rep.findall(html.text)
                        users = pattern_use.findall(html.text)
                        for commit in commits:
                            print commit
                            commit = 'https://github.com'+commit
                            urll.append(commit)
                        for reposite in reposites:
                            print reposite
                            urll.append(reposite)
                        for user in users:
                            print user
                            user = 'http://github.com'+user
                            urll.append(user)
                    except Exception as e:print e

    for list in urll:
        if 'github.com'  in list:
            if list not in urll2:
                urll2.append(list)
                f.write(list + '\n')
    f.close()
#def github_api():#在调用api进行搜索的时候发现，搜索仓库和用户是直接可以的，但是发现搜索其他的就不可以了，查看资料有shell脚本的调用方法参见https://developer.github.com/v3/search/#search-users
    #https://api.github.com/search/users?q=alibaba 搜索用户   所以，我在想，要不要用os模块去调用，然后搜索
    #https://api.github.com/search/repositories?q=alibaba 搜索仓库
    # https://api.github.com/search/issues?q=alibaba 搜索问题 事实证明，api搜索的结果就是shi，不写了
    #header = {"Authorization": "de05fdbefd8888e8685bd7330d5bbf62e56bc5e7"}
    #user = requests.get('https://api.github.com/search/repositories?q=alibaba', headers=header).json()
    #print user
def mayun(): #这个是从码云上查找代码泄露的脚本
    codel = []
    code2 = []
    f_code = open('mayun.txt','wb')
    for line in keyword:
        for page in range(1,10):
            url = 'https://gitee.com/search?group_id=&page='+str(page) +'&search='+line
            print url
            try:
                res = requests.get(url,headers=headers,timeout = 5)
                pattern_my = re.compile(r'</a><a href="(.*?)/w')#正则匹配，这个匹配有点问题，如果用户是w开头的话，就会导致匹配不到，我也在思考能不能减少误杀，又不想多写代码
                mycode = pattern_my.findall(res.text)
                codel.append(line + '\n')
                for code in mycode:
                    code = "https://gitee.com"+code
                    print code
                    codel.append(code)
            except Exception as e:print e
    for code in codel:
        if code not in code2:
            code2.append(code)
            f_code.write(code + '\n')
    f_code.close()
#def csdn():
    # https://code.csdn.net/explore/projects 现在没办法用户啊，一搜索就500
# def taobao() 等等，现在搜索是502.。。http://code.taobao.org/search/
def svnchina():# svn中国代码泄露排查，一般很少发现，就不用页数排列了
    f_svn = open('svnchina.txt','wb')
    for line in keyword:
        url = "http://www.svnchina.com/project_open.php?search%5Bproject_name%5D="+line
        print url
        try:
            res = requests.get(url,headers=headers,timeout=5)
            pattern_my = re.compile(r'http://www.svnchina.com(.*?)<br>')  # 正则匹配
            mycode = pattern_my.findall(res.text)
            for code in mycode:
                code = 'http://www.svnchina.com'+code
                f_svn.write(code+'\n')
        except Exception as e:print e
    f_svn.close()
def thinksaas():# thinksaas开源社区代码排查
    f_think = open('thinksaas.txt','wb')
    codel = []
    code2 = []
    for line in keyword:
        for page in range(0,5):#一般不超过5页
            for id in range(1,5):#id不同搜索的内容不同
                url = 'http://s.thinksaas.cn/cse/search?s=8638015022651739653&nsid='+ str(id) +'&q='+line+'&p='+str(page)
                print url
                codel.append(line+'\n')
                try:
                    res = requests.get(url,headers=headers,timeout = 5)
                    pattern_my = re.compile(r'cpos="title" href="(.*?)"')  # 正则匹配
                    mycode = pattern_my.findall(res.text)
                    for code in mycode:
                        print code
                        codel.append(code)
                except Exception as e:print e
    for code in codel:
        if code not in code2:
            code2.append(code)
            f_think.write(code+'\n')
    f_think.close()
def oschina():#开源中国的代码泄露
    codel = []
    code2 = []
    f_oschina = open('oschina.txt','wb')
    for line in keyword:
        for page in range(1,5):
            url = 'https://www.oschina.net/search?scope=all&q='+ line + '&p='+str(page)
            print url
            try:
                res = requests.get(url,headers=headers,timeout=5)
                pattern_my = re.compile(r'</em><a href=(.*?) target=') # 正则匹配
                mycode = pattern_my.findall(res.text)
                codel.append(line+'\n')
                for code in mycode:
                    code = code.strip("\'")
                    codel.append(code)
            except Exception as e:print e
    for code in codel:
        if code not in code2:
            f_oschina.write(code+'\n')
    f_oschina.close()
def githubpre():  # github工具githubprey信息泄露  把该工具https://github.com/repoog/GitPrey放到linux下的/root/scan/xielou/，在config文件中输入你的github账户名密码
    for target in keyword:
        try:
            a = subprocess.Popen('python GitPrey.py -l 5 -k ' + target + '>>xxx.log', stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, shell=True, cwd='/root/scan/xielou/GitPrey')
            e = a.stdout.readlines()  # 执行shell命令，调用githubpre探测信息泄露
        except:pass
    os.system('cp /root/scan/xielou/GitPrey/xxx.log /root/xxx/code_dis')


if __name__=="__main__":
    github_sousuo()
    mayun()
    svnchina()
    thinksaas()
    oschina()
    githubpre()

