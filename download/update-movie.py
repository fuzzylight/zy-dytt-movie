#coding:utf-8

import urllib
import urllib2
import re
        
file_name = open('fytt.txt','w')
movielist = []
def save2(url, name):
    print ">>> ",name,"  <<< >>>  ", url,"  <<<"
    global file_name
    file_name.write("电影名字："+name+"\n")
    file_name.write("电影链接："+url+"\n")


def get_info( url):
    response = urllib2.urlopen(url)
    content = response.read()
    content = content.decode('gbk','ignore')

    #获得名字
    title_re = re.compile('<font color=#07519a>(.*?)</font>')
    title = title_re.findall(content)    

    #发布时间
    publishdate_re = re.compile(u'发布时间：(\d{4}-\d{2}-\d{2})')
    publishdates = publishdate_re.findall(content)   

    #list 电影海报图 多个取imageurl[-1]
    imageurl_re = re.compile(u'<span style="FONT-SIZE: 12px">([\s\S]*?)◎')
    imageurl = imageurl_re.findall(content)
    if imageurl:
        imageurl_re = re.compile(u'[\s\S]*?src="(.*?)"[\s\S]*?')
        imageurl = imageurl_re.findall(imageurl[0])  

    # list 译名.
    chname_re = re.compile(u'<span style="FONT-SIZE: 12px">[\s\S]*?◎[译|又]　　名\s*?([\s\S]+?)<[\s\S]*?◎片')
    chname = chname_re.findall(content)
    if chname:
        chname = chname[0].split('/')       

    #list 片名.
    name_re = re.compile(u'◎片　　名[　]+?([\s\S]+?)<[\s\S]*?◎年')
    name = name_re.findall(content)
    if name:
        name = name[0].split('/')

    #  类别
    Type_re = re.compile(u'◎类　　[别|型][　]+?([\s\S]+?)<[\s\S]*?◎语')
    Type = Type_re.findall(content)
    

    
    language



    

    #下载链接
    url_re = re.compile('<td.+?bgcolor="#fdfddf"><a href="(.+?)">')
    download_urls = url_re.findall(content)    


    '''
    上面是正则
    ---
    下面是输出
    '''
    
    print title[0].encode('utf8')
    
    
'''
    print publishdates
    if imageurl:
        print imageurl[-1]
        
    print chname[0].encode('utf8')
    print name[0].encode('utf8')
    print Type[0].encode('gbk')


    
    if names and download_urls:
        save2(download_urls[0].decode('gbk').encode('utf8'),names[0].decode('gbk').encode('utf8'))
'''

def run( url):
    response = urllib2.urlopen(url)
    content = response.read()
    ft = re.compile('<a href="(.*?)" class="ulink">')
    urls = ft.findall(content)
    for item in urls:
        new_url = 'http://www.ygdy8.net' + item
        get_info(new_url)

def get_page_number():
    url = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
    response = urllib2.urlopen(url)
    content = response.read()
    url_re = re.compile(u'共(\d*?)页')
    number = url_re.findall(content.decode('gbk','ignore'))
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
    print '共',page_number,'页'
    for i in range(page_number):
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_'+str(i+1) + '.html'
        print "第 ",i+1," 页正在下载"
        run(url)

file_name.close()

