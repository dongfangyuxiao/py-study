
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGl0eSI6IjI2MDI1ODcwNTFAcXEuY29tIiwiaWF0IjoxNTI3NDAxNDYxLCJuYmYiOjE1Mjc0MDE0NjEsImV4cCI6MTUyNzQ0NDY2MX0.jWVeB8GRwG7MgUfUmvsZBoaGbHtv61uA21V34cIK6rE"

header = {'Authorization' : 'JWT '+access_token}
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
word = ['taobao']
f = open('test.json','wb')
for wo in word:
    url = "https://api.zoomeye.org/host/search?query="+ str(wo) +"&page=3"
    r = requests.get(url,headers = header)
    #a = (r.content().decode('utf-8'))
    a = json.loads(r.content)
    for x in a['matches']:
        print x['ip']
        print x['portinfo']['port']