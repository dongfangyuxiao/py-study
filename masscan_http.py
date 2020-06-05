#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import lxml
import queue
import requests
import threading
import re
import os
import nmap
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup
selfurls = []
headers = {
            'Accept': '*/*',
            'Referer': 'http://www.google.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
            'Cache-Control': 'no-cache',
        }
class PortScan(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self._queue = queue

    def run(self):
        while not self._queue.empty():
            scan_ip = self._queue.get()
            try:
                scan(scan_ip)
            except Exception as e:
                print (e)
                pass


def scan(scan_ip):
    ip = scan_ip.split(':')[0]
    port = str(scan_ip.split(':')[1])
    line = 'http://'+scan_ip
    line2 = 'https://'+scan_ip
    verify(line)
    verify(line2)
    service(ip,port)

def service(ip,port):
    attackservices= ['irc', 'sshkey', 'ldap3', 'mysql', 'telnetcpcd', 'mongodb', 'xmpp', 'ms-olap2', 'firebird', 'nntp', 'rsqlserver', 'mysql-cm-agent', 'cisco', 'sip', 'mysql-im', 'ldap', 'smtp-enum', 'ssh', 'rsh', 'sqlnet', 'ftp-data', 'adam6500', 'mysql-cluster', 'socks5', 'svn', 'ms-olap1', 's7-300', 'sossd-collect', 'vnc', 'pcnfs', 'rtsp', 'vmauthd', 'teamspeak', 'sphinxql', 'ftp', 'cvs', 'postgres', 'icq', 'rexec', 'rtelnet', 'smb', 'telnet', 'mssql', 'sftp', 'stel', 'ajp12', 'imap', 'ajp13', 'ktelnet', 'ftps-data', 'smtps', 'oracle-listener', 'imaps', 'cisco-enable', 'rpcap', 'radmin2', 'sqlserv', 'sql-net', 'msql', 'sossd-agent', 'asterisk', 'rdp', 'redis', 'oracle-sid', 'rlogin', 'sqlsrv', 'pcanywhere', 'pop', 'ldap2', 'telnets', 'ftps', 'pop3s', 'snmp', 'mysql-proxy', 'sossd-disc', 'memcached', 'mysqlx', 'rsync']
    nm = nmap.PortScanner()
    ret = nm.scan(ip, port, arguments='-Pn,-sS')
    service_name = service_name = ret['scan'][ip]['tcp'][int(port)]['name']
    if service_name.lower() in attackservices:
        write_service(ip+','+str(port)+','+service_name)

def verify(url):
        #print url
    try:
        res = requests.get(url,headers = headers,verify=False,timeout=10)
        response = re.findall(u'<title>(.*?)</title>', res.content.decode("utf-8"))

        if res.status_code==200:
            if response:
                _write_title(res.url + ',' + response[0])
            else:
                _write_title(res.url + ',' + str(len(res.content)))
            if res.url not in selfurls:
                _write200(res.url)
                selfurls.append(res.url)

        elif not str(res.status_code).startswith('5') and res.status_code!=400:
            if res.url not in selfurls :
                selfurls.append(res.url)

                _writehttp(res.url)

    except Exception as e:
        pass
def _writehttp(url):
        with open('ip_http.txt', 'a+') as f:
            f.write(url + '\t\n')
def _write_title(line):
    with open('ip_tilte.txt', 'a+') as f:
        f.write(line + '\t\n')

def _write200(url):

        with open('ip_200.txt','a+') as f:
            f.write(url+'\t\n')

def write_service(line):
    f = open('ip_service.txt','a+')
    f.write(line+'\t\n')


def masscan_fin():
    temp_ports = []
    fd = open('fofa_ip.txt', 'rb')
    for line in fd.readlines():
        temp_ports.append(line.decode("utf-8").strip())
    if len(temp_ports) < 1000:
        ports = '1-59999'
        rate='2000'
    elif len(temp_ports) < 2500:
        ports = '1-49999'
        rate='5000'
    elif len(temp_ports) < 5000:
        ports = '1-39999'
        rate='10000'
    elif len(temp_ports) < 10000:
        ports = '1-29999'
        rate='12000'
    else:
        ports = '1-19999'
        rate = '15000'
    os.system('masscan -iL all_ip.txt' + ' -p ' + ports + '  -oL masscan.txt --rate '+rate)

def main():
    masscan_fin()
    q = queue.Queue()
    q2 = queue.Queue()
    with open('masscan.txt') as f:
        for line in f:
            lins = line.strip().split(' ')
            if 'open' in line:
                lins = line.strip().split(' ')
                zuhu = lins[3] + ':' + lins[2]
                q.put(zuhu)

    print(q.qsize())
    threads = []
    thread_count = 100
    for i in range(thread_count):
        threads.append(PortScan(q))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    f.close()

if __name__ == "__main__":
    main()




