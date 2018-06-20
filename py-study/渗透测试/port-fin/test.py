#!/usr/bin/python
# -*- coding:utf-8 -*-
# for:
# user:xiaodong
# usage:
# tool:pycharm

import subprocess

import requests

from subprocess import *


p = subprocess.Popen('ping baidu.com -c 4',shell=True, stdout=subprocess.PIPE)

out = p.stdout.read()

print out
