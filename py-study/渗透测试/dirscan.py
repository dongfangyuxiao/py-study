#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author  : xiaodong
# @Site    : 
# @File    : dirscan.py
# @Software: PyCharm

__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'


import time
import sys
import subprocess
import threading
import Queue

class Dirscan(threading.Thread):


    def __init__(self, que):
        threading.Thread.__init__(self)
        self._que = que
        self.qd = []
        self.dir = []


    def BBscan(self,url):

        try:
            a= subprocess.Popen('python BBScan.py --host '+ url,shell=True, stdout=subprocess.PIPE, cwd='/root/scan/dirscan/BBScan')
            data = a.stdout.read()
            if '200' in data:
                self.dir.append(data)
                print 'BBScan found {}'.format(data)
            else:print 'sorry no dir '
        except Exception as e:
            print e

    def webdirscan(self,url):
        try:
            a = subprocess.Popen('python webdirscan.py -t 100 ' + url, shell=True, stdout=subprocess.PIPE,
                                 cwd='/root/scan/dirscan/webdirscan')
            data = a.stdout.read()
            if '200' in data:
                self.dir.append(data)
                print "webdirscan found {}".format(data)
            else: print "sorry"
        except Exception as e:
            print e

    def weakfilescan(self,url):
        try:
            a = subprocess.Popen('python weakfilescan.py -t 100 ' + url, shell=True, stdout=subprocess.PIPE,
                                 cwd='/root/scan/dirscan/webdirscan')
            data = a.stdout.read()
            if '200' in data:
                self.dir.append(data)
                print "weakfilescan found {}".format(data)
            else: print "sorry"
        except Exception as e:
            print e

    def ok_write(self):
        f = open('/project/scan/dirscan/200_http.txt','wb')
        for line in self.dir:
            f.write(line+ '\n')






    def run(self):
        while not self._que.empty():
            url = self._que.get()
            self.BBscan(url)
            self.webdirscan(url)
            self.weakfilescan(url)
        self.ok_write()





def main():
    que = Queue.Queue()
    threads = []
    thread_count = 20
    f = open('/root/project/info/port/http.txt','rb')
    for line in f:
        line = line.strip()
        que.put(line)

    for i in range(thread_count):
        threads.append(Dirscan(que))

    for i in threads:
        i.start()
    for i in threads:
        i.join()

if __name__ == '__main__':
    main()



