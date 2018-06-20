#!/usr/bin/python
# -*- coding:utf-8 -*-
# for:
# user:xiaodong
# usage:
# tool:pycharm

def install_package():
    try: #not always working in different pip version,eg. pip 10.0.1
        import pip
        installed_packages = pip.get_installed_distributions()
        flat_installed_packages = [package.project_name for package in installed_packages]
        requirements = open("requirements.txt","r").readlines()
        for require in requirements:
            if require.strip() in flat_installed_packages:
                pass
            else:
                pip.main(['install', require])
    except Exception,e:
        print("Install {0} failed, Please check.")

#install_package()

import argparse
import datetime
import os
import threading
import Queue
import sys

from infog.teemo import teemo
from infog.subDomainsBrute import subDomainsBrute
from infog.sublist3r import sublist3r
from infog.fierce import fierce

from infog.theharvester import theharvest

reload(sys)
sys.setdefaultencoding('utf-8')
sys.dont_write_bytecode = True

#In case you cannot install some of the required development packages, there's also an option to disable the SSL warning:
try:
    import requests.packages.urllib3
    requests.packages.urllib3.disable_warnings()
except:
    pass


def parser_error(errmsg):
    print ("Usage: python "+sys.argv[0]+" [Options] use -h for help")
    sys.exit()

def parse_args(): #optparse模块从2.7开始废弃，建议使用argparse
    parser = argparse.ArgumentParser(epilog = '\tExample: \r\npython '+sys.argv[0]+" -d google.com")
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    parser.add_argument('-d', '--domain', help="Domain name to enumrate it's subdomains", required=True)
    parser.add_argument('-o', '--output', help='Save the results to text file')

    return parser.parse_args()

def adjust_args():
    args = parse_args()
    # Validate domain

    if not args.output:
        now = datetime.datetime.now()
        timestr = now.strftime("-%Y-%m-%d-%H-%M")
        args.output = args.domain + timestr + ".txt"
    args.output = os.path.join(os.path.dirname(__file__), "output", args.output)



    return args

def callengines_thread(engine, key_word, q_domains, q_emails,q_ips,q_ipcs):
    x = engine(key_word)
    domains,emails,ips,ipcs = x.run()
    if domains: # domains maybe None
        for domain in domains:
            q_domains.put(domain)
    if emails:
        for email in emails:
            q_emails.put(email)
    if ips:
        for ip in ips:
            q_ips.put(ip)
    if ipcs:
        for ipc in ipcs:
            q_ipcs.put(ipc)


def main():
    try:
        args = adjust_args()

        print "[-] Enumerating subdomains now for %s" % args.domain

        #doing zone transfer checking


        Threadlist = []
        q_domains = Queue.Queue() #to recevie return values,use it to ensure thread safe.
        q_ips = Queue.Queue()
        q_ipcs = Queue.Queue()
        q_emails = Queue.Queue()



        for engine in [teemo,subDomainsBrute,sublist3r,fierce,theharvest]:
            t = threading.Thread(target=callengines_thread, args=(engine, args.domain, q_domains, q_emails,q_ips,q_ipcs))
            t.setDaemon(True) #变成守护进程，独立于主进程。这里好像不需要
            Threadlist.append(t)

        #for t in Threadlist:
        #    print t
        for t in Threadlist: # use start() not run()
            t.start()
        for t in Threadlist: #为什么需要2次循环，不能在一次循环中完成？
            t.join() #主线程将等待这个线程，直到这个线程运行结束


        subdomains = []
        while not q_domains.empty():
            subdomains.append(q_domains.get())
        subdomains = list
        emails = []
        while not q_emails.empty():
            emails.append(q_emails.get())
        related_domains =[]
        ips = []
        while not q_ips.empty():
            ips.append(q_ips.get())
        ipcs = []
        while not q_ipcs.empty():
            ipcs.append(q_ipcs.get())

        subdomains_new = []
        emails_new = []
        ips_new = []
        ipcs_new = []

        for subdomain in subdomains:
            if subdomain not in subdomains_new:
                subdomains_new.append(subdomain)
                print subdomain
        for email in emails:
            if email not in emails_new:
                emails_new.append(email)
                print email
        for ip in ips:
            if ip not in ips_new:
                ips_new.append(ip)
                print ip
        for ipc in ipcs:
            if ipc not in ipcs_new:
                ipcs_new.append(ipc)
                print ipc


        fd = open('/root/project/info/domain_all.txt',"wb")
        fe = open('/root/project/info/email_all.txt', "wb")
        fi = open('/root/project/info/ip_all.txt', "wb")
        fs = open('/root/project/info/ipc_all.txt', "wb")
        #fp.writelines("\n".join(subdomains).decode("utf-8"))
        fd.writelines("\n".join(subdomains_new).encode("utf-8"))
        fe.writelines("\n".join(emails_new).encode("utf-8"))
        fi.writelines("\n".join(ips_new).encode("utf-8"))
        fs.writelines("\n".join(ipcs_new).encode("utf-8"))
        subdomain_number = len(subdomains_new)

        print "[+] {0} domains found in total".format(subdomain_number)
        print "[+] {0} ip found in total".format(len(ips_new))
        print "[+] {0} emails found in total".format(len(emails_new))
        print "[+] {0} ipc found in total".format(len(ipcs_new))
        print "[+] Results saved to {0}".format(args.output)
    except KeyboardInterrupt as e:
        print "Exit. Due To KeyboardInterrupt"


if __name__=="__main__":
    main()
