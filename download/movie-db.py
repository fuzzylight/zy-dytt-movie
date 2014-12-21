#coding:utf-8

import urllib
import urllib2
import re
import time
import json
import proxyIP,user_agents
import random
import MySQLdb

Count = {}



def get_title(content):
    """ 获得标题名字 """
    title_re = re.compile(u'<font color=#07519a>(.*?)</font>')
    title = title_re.findall(content)
    if title:
        title = title[0].encode('gbk')
    else:
        title = None
    print title
    return title

def get_publishdate(content):
    """发布时间"""
    publishdate_re = re.compile(u'发布时间：(\d{4}-\d{2}-\d{2})')
    publishdate = publishdate_re.findall(content)
    if publishdate:
         publishdate = publishdate[0].encode('gbk')
    else:
        publishdate == None
    return publishdate

def get_imageurl(content):
    """list 电影海报图 多个取imageurl[-1]"""
    imageurl_re = re.compile(u'<span style="FONT-SIZE: 12px">([\s\S]*?)◎')
    imageurl = imageurl_re.findall(content)
    if imageurl:
        imageurl_re = re.compile(u'[\s\S]*?src="(.*?)"[\s\S]*?')
        imageurl = imageurl_re.findall(imageurl[0])
    if imageurl:
        imageurl = imageurl[-1].encode('gbk')
    else:
        imageurl = None
    return imageurl

def get_chname(content):
    """ list 译名."""
    chname_re = re.compile(u'<span style="FONT-SIZE: 12px">[\s\S]*?◎[译|又]　　名\s*?([\s\S]+?)<[\s\S]*?◎片')
    chname = chname_re.findall(content)
    if chname:
        chname = chname[0].split('/')
    l = len(chname)
    for i in range(l):
        chname[i] = chname[i].encode('gbk')
    return chname

def get_name(content):
    """list 片名."""
    name_re = re.compile(u'◎片　　名[　]+?([\s\S]+?)<[\s\S]*?◎年')
    name = name_re.findall(content)
    if name:
        name = name[0].split('/')
    l = len(name)
    for i in range(l):
        name[i] = name[i].encode('gbk')
    return name

def get_type(content):
    """类别"""
    Type_re = re.compile(u'◎类　　[别|型][　]+?([\s\S]+?)<[\s\S]*?◎语')
    Type = Type_re.findall(content)
    if Type:
        Type = Type[0].encode('gbk')
    else:
        Type = None
    return Type

def get_language(content):
    """语言"""
    language_re = re.compile(u'◎语　　言[　]+?([\s\S]+?)<[\s\S]*?◎')
    language = language_re.findall(content)
    if language:
        language = language[0].encode('gbk')
    else:
        language = None
    return language

def get_subtitles(content):
    """字幕"""
    subtitles_re = re.compile(u'◎字　　幕[　]+?([\s\S]+?)<[\s\S]*?◎')
    subtitles = subtitles_re.findall(content)
    if subtitles:
        subtitles = subtitles[0].encode('gbk')
    else:
        subtitles = None
    return subtitles

def get_fileformat(content):
    #文件格式
    fileformat_re = re.compile(u'◎文件格式[　]+?([\s\S]+?)<[\s\S]*?◎')
    fileformat = fileformat_re.findall(content)
    if fileformat:
        fileformat = fileformat[0].encode('gbk')
    else:
        fileformat = None
    return fileformat

def get_width(content):
    """视频尺寸，我们要的是视频尺寸width"""
    moviesize_re = re.compile(u'◎视频尺寸[　]+?([\s\S]+?)<[\s\S]*?◎')
    moviesize = moviesize_re.findall(content)
    if moviesize:
        width_re = re.compile(u'(\d*?) x \d*?')
        width = width_re.findall(moviesize[0])
        if width:
            width = width[0].encode('gbk')
        else:
            width = None
    else:
        width = None
    return width

def get_height(content):
    """视频尺寸，我们要的是视频尺寸height"""
    moviesize_re = re.compile(u'◎视频尺寸[　]+?([\s\S]+?)<[\s\S]*?◎')
    moviesize = moviesize_re.findall(content)
    if moviesize:
        height_re = re.compile(u'\d*? x (\d*?)')
        height = height_re.findall(moviesize[0])
        if height:
            height = height[0].encode('gbk')
        else:
            height = None
    else:
        height = None
    return height

def get_size(content):
    """文件大小"""
    size_re = re.compile(u'◎文件大小[　]+?([\s\S]+?)<[\s\S]*?◎')
    size = size_re.findall(content)
    if size:
        size = size[0].encode('gbk')
    else:
        size = None
    return size

def get_duration(content):
    """片长"""
    duration_re = re.compile(u'◎片[ 　]+?长[　]+?([\s\S]+?)<[\s\S]*?◎')
    duration = duration_re.findall(content)
    if duration:
        duration = duration[0].encode('gbk')
    else:
        duration = None
    return duration

def get_director(content):
    """导演"""
    director_re = re.compile(u'◎导　　演[　]+?([\s\S]+?)<[\s\S]*?◎')
    director = director_re.findall(content)
    if director:
        director = director[0].encode('gbk')
    else:
        director = None
    return director

def get_actors(content):
    """list  主演     凯特·贝金赛尔  中间的点会出现问题"""
    actors_re = re.compile(u'◎主　　演([\s\S]+?)◎')
    actors = actors_re.findall(content)
    if actors:
        actors = actors[0].split('<br />')
        l = len(actors)
        for i in range(l):
            actors[i] = actors[i].strip()
            actors[i] = actors[i].encode('gbk')
    return actors

def get_introduce(content):
    """简介"""
    introduce_re = re.compile(u'◎[简|簡]　　介([\s\S]*?)◎')
    introduce = introduce_re.findall(content)
    if not introduce:
        introduce_re = re.compile(u'◎[简|簡]　　介([\s\S]*?)<img')
        introduce = introduce_re.findall(content)

    if not introduce:
        introduce_re = re.compile(u'◎[简|簡]　　介([\s\S]*?)</p>')
        introduce = introduce_re.findall(content)
    if introduce:
        introduce = introduce[0]
        introduce = introduce.split('<br />')
        l = len(introduce)
        for i in range(l):
            introduce[i] = introduce[i].encode('gbk')
    else:
        introduce = None
    
    return introduce

def get_introduceimageurl(content):
    """介绍图"""
    introduceimageurl_re = re.compile(u'◎片　　名[\s\S]*?src="(.*?)"[\s\S]*?</p>')
    introduceimageurl = introduceimageurl_re.findall(content)
    if introduceimageurl:
        introduceimageurl = introduceimageurl[0].encode('gbk')
    else:
        introduceimageurl = None
    return introduceimageurl

def get_downloadlink(content):
    """下载链接"""
    downloadlink_re = re.compile('<td.+?bgcolor="#fdfddf"><a href="(.+?)">')
    downloadlink = downloadlink_re.findall(content)   
    if downloadlink:
        downloadlink = downloadlink[0].encode('gbk')
    else:
        downloadlink = None
    return downloadlink


# ------------我是华丽的分割线-----------------------------

def set_Count():
    global Count
    Count['movies'] = 0
    Count['chnames'] = 0
    Count['names'] = 0
    Count['types'] = 0
    Count['languages'] = 0
    Count['actors'] = 0
    Count['introduces'] = 0
    Count['iiurls'] = 0
    Count['durls'] = 0

def save_movie(con):
    movie = {}
    movie["title"] = get_title(con)
    movie["publishdate"] = get_publishdate(con)
    movie["imageurl"] = get_imageurl(con)
    movie["chname"] = get_chname(con)
    movie["name"] = get_name(con)
    movie["type"] = get_type(con)
    movie["language"] = get_language(con)
    movie["subtitles"]= get_subtitles(con)
    movie["fileformat"]= get_fileformat(con)
    movie["width"] = get_width(con)
    movie["height"] = get_height(con)
    movie["size"] = get_size(con)
    movie["duration"] = get_duration(con)
    movie["director"] = get_director(con)
    movie["actors"] = get_actors(con)
    movie["introduce"] = get_introduce(con)
    movie["introduceimageurl"] = get_introduceimageurl(con)
    movie["downloadlink"] = get_downloadlink(con)
    print movie['title']
    return movie

    


def get_page_info( url):
    """得到网页信息"""
    try:
        randomTime = random.uniform(0,1)
        time.sleep(randomTime)
        
        proxy_ip = random.choice(proxyIP.proxy_list)
        print proxy_ip
        proxy_support = urllib2.ProxyHandler(proxy_ip)
        opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)
        urllib2.install_opener(opener)
        request = urllib2.Request(url)
        user_agent = random.choice(user_agents.user_agents)
        print user_agent
        req = urllib2.Request(url,headers=user_agent)
        html = urllib2.urlopen(req)

        if url == html.geturl():
            content = html.read()
            content = content.decode('gbk','ignore')
            return content
    except:
        return get_page_info(url)

def save(movie):
    global Count
    Count['movies'] = Count['movies']+1
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',db='dyttmovie',port=3306,charset='gbk')
    cur=conn.cursor()

    #插入总表
    values = []
    values.append(Count['movies'])
    values.append(movie['title'])
    values.append(movie['publishdate'])
    values.append(movie['imageurl'])
    values.append(movie['subtitles'])
    values.append(movie['fileformat'])
    values.append(movie['width'])
    values.append(movie['height'])
    values.append(movie['size'])
    values.append(movie['duration'])
    values.append(movie['director'])
    print values
    cur.execute('insert into movies values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',values)



    
    conn.commit()
    
    cur.close()
    conn.close()
    
    

def run( url):
    content = get_page_info(url)
    ft = re.compile('<a href="(.*?)" class="ulink">')
    urls = ft.findall(content)
    for item in urls:
        new_url = 'http://www.ygdy8.net' + item
        content = get_page_info(new_url)
        movie = save_movie(content)
        save(movie)

def get_page_number():
    url = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
    content = get_page_info(url)
    url_re = re.compile(u'共(\d*?)页')
    number = url_re.findall(content)
    return int(number[0])


if __name__ == '__main__':
    set_Count()
    page_number = get_page_number()
    print '共',page_number,'页'
    for i in range(10):
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_'+str(i+1) + '.html'
        print "第 ",i+1," 页正在下载"
        run(url)
    save()



