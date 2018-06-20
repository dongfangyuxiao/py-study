__author__ = 'xiaodong'
__github__ = 'https://github.com/dongfangyuxiao/'
import requests
from lib import config
from lib import myrequest
req = myrequest
import re
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from bs4 import BeautifulSoup
# https://api.zoomeye.org/host/search?query=
class search_zoomeye():
    def __init__(self,word,proxy=None):
        self.engine_name = 'zoomeye'
        self.server = 'api.zoomeye.org'
        self.counter = 1
        self.proxies = proxy
        self.catagory = ""
        self.limit = 100
        self.type = ""
        self.word = word.replace(' ','%20')
        self.result = ""
        self.totalresults = ""
        self.print_banner()
        return

    def print_banner(self):
        print "Searching now in {0}..".format(self.engine_name)
        return

    def auto_login(self):
        """
        Get cookie for logining GitHub
        :returns: None
        """
        data_info = {'username': '2602587051@qq.com', 'password': 'XXXXXX'}
        # dumps() -> python'object cast the type of json
        data_encoded = json.dumps(data_info)

        # POST
        respond = requests.post(url='https://api.zoomeye.org/user/login', data=data_encoded)

        try:
            # loads() -> json cast python'object
            r_decoded = json.loads(respond.text)

            # get access_token
            self.token  = r_decoded['access_token']
        except KeyError:
            return 'ErrorInfo'

        return self.token

    def do_search(self):
        self.token = self.auto_login()

        #print self.cookies
        header = {'Authorization': 'JWT ' + self.token}

        ul = 'https://api.zoomeye.org/host/search?query='+self.word
        # print ul
        res = req.get(ul, headers=header, timeout=5)
        # print res.status_code
        count = re.findall(r'"available":(.*?),', res.text)
        print count
        cou = int(count[0])
        cou = cou // 20
        for page in range(1, cou + 2):
            url = 'https://{0}/host/search?query={1} &page={2}'.format(self.server,self.word,page)
            # print url
            respond = requests.get(url, headers=header, timeout=5)
            self.result = respond.content
            self.totalresults=self.result + self.totalresults
    def get_url(self):
        urls = []
        pattern_ip = re.compile('"ip": "(.*?)",')
        pattern_port = re.compile('"port": (.*?),')
        ipl = pattern_ip.findall(self.totalresults)
        portl = pattern_port.findall(self.totalresults)
        #print len(ipl)
        #print len(portl)

        for x in range(300):#
            line = ipl[x].strip()+':'+portl[x].strip()
            #print line
            url = 'http://'+line +'/'
            try:
                r = req.get(url)
                if r.status_code == '200':
                    urls.append(url)
            except Exception,e:
                pass

        return urls





    def run(self):
        try:
            self.do_search()
            self.d = self.get_url()
            return self.d
        finally:
            print "{} found {} links ".format(self.engine_name, len(self.d))



if __name__ == "__main__":
    seach = search_zoomeye("alibaba")
    seach.run()