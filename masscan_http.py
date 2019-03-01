#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import lxml
import Queue
import requests
import threading
from bs4 import BeautifulSoup
class Myhttp(object):
    def __init__(self,):
        self.load_url()
        self._loadHeaders()
        self.lock = threading.Lock()


    def load_url(self):
        self.q = Queue.Queue()
        with open('/root/project/masscan/masscan_port.txt') as f:
            for line in f:
                lins = line.strip().split(' ')
                if '443' in line:
                    url = 'https://' + lins[5] + ':' + lins[3].strip('\/tcp')
                else:
                    url = 'http://' + lins[5] + ':' + lins[3].strip('\/tcp')

                self.q.put(url)

    def _loadHeaders(self):
        self.headers = {
            'Accept': '*/*',
            'Referer': 'http://www.baidu.com',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
            'Cache-Control': 'no-cache',
        }

    def _writehttp(self, url):
        self.lock.acquire()
        with open('ip_http.txt', 'a+') as f:
            f.write(url + '\n')
        self.lock.release()
    def _write200(self,url):
        self.lock.acquire()
        with open('ip_200.txt','a+') as f:
            f.write(url+'\n')
        self.lock.release()
    def _writenohttp(self, url):
        self.lock.acquire()
        with open('ip_nohttp.txt', 'a+') as f:

            f.write(url + '\n')
        self.lock.release()
    def verify(self,url):
        #print url
        try:
            res = requests.get(url,headers = self.headers,verify=False,timeout=3)
            if res.status_code==200:
                self._write200(url)
                #self._writehttp(url)
            if res.status_code==302:#这个是根据真实c段和ip扫描的结果，所以只要有返回值就保存
                self._write200(url)
            else:
                pass

        except Exception as e:
            pass
            #print e
            #self._writenohttp(url)
    def run(self):
        while not self.q.empty():
            url = self.q.get()
            #print url
            self.verify(url)

if __name__ == "__main__":
    scan = Myhttp()
    for i in range(10):
        t = threading.Thread(target=scan.run)
        t.start()



