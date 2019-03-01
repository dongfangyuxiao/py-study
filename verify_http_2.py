#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 这个写的特别好，又稳定，速度又快
import time
import Queue
import requests
import threading

class Myhttp(object):
    def __init__(self,):
        self.load_url()
        self._loadHeaders()
        self.lock = threading.Lock()


    def load_url(self):
        self.q = Queue.Queue()
        with open('domain_all.txt') as f:
            for line in f:
                line = 'http://' + line.strip()
                self.q.put(line)

    def _loadHeaders(self):
        self.headers = {
            'Accept': '*/*',
            'Referer': 'http://www.baidu.com',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; ',
            'Cache-Control': 'no-cache',
        }

    def _writehttp(self, url):
        self.lock.acquire()
        with open('domain_http.txt', 'a+') as f:
            f.write(url + '\n')
        self.lock.release()
    def _write200(self, url):
        self.lock.acquire()
        with open('domain_200.txt', 'a+') as f:
            f.write(url + '\n')
        self.lock.release()
    def _write302(self, url):
        self.lock.acquire()
        with open('domain_302.txt', 'a+') as f:
            f.write(url + '\n')
        self.lock.release()
    def verify(self,url):
        #print url
        try:
            res = requests.get(url,headers = self.headers,verify=False,timeout=3)
            if res.status_code ==200:
                
                self._write200(url)
                self._writehttp(url)
                #else:
                   # self._writehttp(url)
            #if res.status_code ==302:
                #self._write302(url)

            else:
                self._writehttp(url)

        except Exception as e:
            pass
    def run(self):
        while not self.q.empty():
            url = self.q.get()
            self.verify(url)

if __name__ == "__main__":
    scan = Myhttp()
    #for i in range(200):
        #t = threading.Thread(target=scan.run)
        #t.start()
    print scan.run()



