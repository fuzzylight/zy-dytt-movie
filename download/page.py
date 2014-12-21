#coding:utf-8

import urllib
import urllib2
import re


url = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'


proxy = {'http':'http://218.108.170.171:82'}
proxy_support = urllib2.ProxyHandler(proxy)
opener = urllib2.build_opener(proxy_support)
urllib2.install_opener(opener)

i_headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.48'}
req = urllib2.Request(url,headers=i_headers)

response = urllib2.urlopen(req)
content = response.read()
print content
