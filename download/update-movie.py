#coding:utf-8

import urllib
import urllib2
import re


'''
def save(url, name): # 数据库还没写.
   conn = MySQLdb.connect(host = 'localhost', user = 'root', passwed= '',db = "dyttdb")
    cursor = conn.cursor()

    sql = "insert into dytt(name, url) values(%s, %s)"
    param = (name, url)
    cursor.execute(sql, param)
'''

file_name = open('fytt.txt','w')

def save2(url, name):
    print ">>> ",name,"  <<< >>>  ", url,"  <<<"
    global file_name
    file_name.write("电影名字："+name+"\n")
    file_name.write("电影链接："+url+"\n")
    
def get_download_url( url):
    response = urllib2.urlopen(url)
    content = response.read()

    url_re = re.compile('<td.+?bgcolor="#fdfddf"><a href="(.+?)">')
    download_urls = url_re.findall(content)
    
    name_re = re.compile('<font color=#07519a>(.*?)</font>')
    names = name_re.findall(content)
    if names and download_urls:
        save2(download_urls[0].decode('gbk').encode('utf8'),names[0].decode('gbk').encode('utf8'))
    
def run( url):
    response = urllib2.urlopen(url)
    content = response.read()
    ft = re.compile('<a href="(.*?)" class="ulink">')
    urls = ft.findall(content)
    for item in urls:
        new_url = 'http://www.ygdy8.net' + item
        get_download_url(new_url)

def get_page_number():
    url = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
    response = urllib2.urlopen(url)
    content = response.read()
    url_re = re.compile(u'共(\d*?)页')
    number = url_re.findall(content.decode('gbk'))
    return int(number[0])

'''
if __name__ == '__main__':
    numa = int(input("从第几页开始下载： "))
    numb = int(input("一直下载到第几页： "))
    for i in range(numa,numb+1):
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_'+str(i) + '.html'
        print "第 ",i," 页正在下载"
        run(url)

file_name.close()
'''

if __name__ == '__main__':
    page_number = get_page_number()
        
    for i in range(page_number):
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_'+str(i+1) + '.html'
        print "第 ",i+1," 页正在下载"
        run(url)

file_name.close()

