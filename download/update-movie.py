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
    

    #语言
    language_re = re.compile(u'◎语　　言[　]+?([\s\S]+?)<[\s\S]*?◎')
    language = language_re.findall(content)
    
    #字幕
    subtitles_re = re.compile(u'◎字　　幕[　]+?([\s\S]+?)<[\s\S]*?◎')
    subtitles = subtitles_re.findall(content)
    

    #文件格式
    fileformat_re = re.compile(u'◎文件格式[　]+?([\s\S]+?)<[\s\S]*?◎')
    fileformat = fileformat_re.findall(content)
    

    #视频尺寸，我们要的是视频尺寸width，height
    moviesize_re = re.compile(u'◎视频尺寸[　]+?([\s\S]+?)<[\s\S]*?◎')
    moviesize = moviesize_re.findall(content)
    if moviesize:
        width_re = re.compile(u'(\d*?) x \d*?')
        width = width_re.findall(moviesize[0])
        height_re = re.compile(u'\d*? x (\d*?)')
        height = width_re.findall(moviesize[0])

    #文件大小
    size_re = re.compile(u'◎文件大小[　]+?([\s\S]+?)<[\s\S]*?◎')
    size = size_re.findall(content)

    #片长
    duration_re = re.compile(u'◎片[ 　]+?长[　]+?([\s\S]+?)<[\s\S]*?◎')
    duration = duration_re.findall(content)

    #导演
    director_re = re.compile(u'◎导　　演[　]+?([\s\S]+?)<[\s\S]*?◎')
    director = director_re.findall(content)
    

    #list  主演     凯特·贝金赛尔  中间的点会出现问题
    actors_re = re.compile(u'◎主　　演([\s\S]+?)◎')
    actors = actors_re.findall(content)
    actors = actors[0].split('<br />')
    l = len(actors)
    for i in range(l):
        actors[i] = actors[i].strip()


    #简介   这里有问题。可能简介下面还有东西，或者没有东西，</p> 和 ◎ 之间或关系。还没搞清楚
    introduce_re = re.compile(u'◎[简|簡]　　介([\s\S]*?)</p>')
    introduce = introduce_re.findall(content)
    introduce = introduce[0].split('<br />')
    

    #介绍图
    introduceimageurl_re = re.compile(u'◎片　　名[\s\S]*?src="(.*?)"[\s\S]*?</p>')
    introduceimageurl = introduceimageurl_re.findall(content)
    
    
    #下载链接
    downloadlink_re = re.compile('<td.+?bgcolor="#fdfddf"><a href="(.+?)">')
    downloadlink = downloadlink_re.findall(content)    


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
    print language[0].encode('gbk')
    if subtitles:
        print subtitles[0].encode('gbk')
    print fileformat
    print size
    print director[0].encode('gbk')
    for actor in actors:
        print actor.encode('gbk')
    for intro in introduce:
        print intro.encode('gbk')
    print introduceimageurl
        

    
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

