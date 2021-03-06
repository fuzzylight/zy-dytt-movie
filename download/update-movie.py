#coding:utf-8

import urllib
import urllib2
import re
import time
import MySQLdb
def createdb():
    conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',charset='utf-8')
    cursor = conn.cursor()
    #如果没有数据库zy-movie,新建一张
    cursor.execute( "create database if not exists zy-movie")
    #选择数据库. 由于连接的时候无法确定是否存在zy-movie，如果没有生成一个.所以现在来选择.
    conn.select_db('zy-movie')

def get_title(content):
    """ 获得标题名字 """
    title_re = re.compile('<font color=#07519a>(.*?)</font>')
    title = title_re.findall(content)
    if title:
        title = title[0]
    else:
        title = None
    print title
    return title

def get_publishdate(content):
    """发布时间"""
    publishdate_re = re.compile(u'发布时间：(\d{4}-\d{2}-\d{2})')
    publishdate = publishdate_re.findall(content)
    if publishdate:
         publishdate = publishdate[0]
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
        imageurl = imageurl[-1]
    else:
        imageurl = None
    return imageurl

def get_chname(content):
    """ list 译名."""
    chname_re = re.compile(u'<span style="FONT-SIZE: 12px">[\s\S]*?◎[译|又]　　名\s*?([\s\S]+?)<[\s\S]*?◎片')
    chname = chname_re.findall(content)
    if chname:
        chname = chname[0].split('/')

    return chname

def get_name(content):
    """list 片名."""
    name_re = re.compile(u'◎片　　名[　]+?([\s\S]+?)<[\s\S]*?◎年')
    name = name_re.findall(content)
    if name:
        name = name[0].split('/')
    return name

def get_type(content):
    """类别"""
    Type_re = re.compile(u'◎类　　[别|型][　]+?([\s\S]+?)<[\s\S]*?◎语')
    Type = Type_re.findall(content)
    if Type:
        Type = Type[0]
    else:
        Type = None
    return Type

def get_language(content):
    """语言"""
    language_re = re.compile(u'◎语　　言[　]+?([\s\S]+?)<[\s\S]*?◎')
    language = language_re.findall(content)
    if language:
        language = language[0]
    else:
        language = None
    return language

def get_subtitles(content):
    """字幕"""
    subtitles_re = re.compile(u'◎字　　幕[　]+?([\s\S]+?)<[\s\S]*?◎')
    subtitles = subtitles_re.findall(content)
    if subtitles:
        subtitles = subtitles[0]
    else:
        subtitles = None
    return subtitles

def get_fileformat(content):
    #文件格式
    fileformat_re = re.compile(u'◎文件格式[　]+?([\s\S]+?)<[\s\S]*?◎')
    fileformat = fileformat_re.findall(content)
    if fileformat:
        fileformat = fileformat[0]
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
            width = width[0]
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
            height = height[0]
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
        size = size[0]
    else:
        size = None
    return size

def get_duration(content):
    """片长"""
    duration_re = re.compile(u'◎片[ 　]+?长[　]+?([\s\S]+?)<[\s\S]*?◎')
    duration = duration_re.findall(content)
    if duration:
        duration = duration[0]
    else:
        duration = None
    return duration

def get_director(content):
    """导演"""
    director_re = re.compile(u'◎导　　演[　]+?([\s\S]+?)<[\s\S]*?◎')
    director = director_re.findall(content)
    if director:
        director = director[0]
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
    else:
        introduce = None
    
    return introduce

def get_introduceimageurl(content):
    """介绍图"""
    introduceimageurl_re = re.compile(u'◎片　　名[\s\S]*?src="(.*?)"[\s\S]*?</p>')
    introduceimageurl = introduceimageurl_re.findall(content)
    if introduceimageurl:
        introduceimageurl = introduceimageurl[0]
    else:
        introduceimageurl = None
    return introduceimageurl

def get_downloadlink(content):
    """下载链接"""
    downloadlink_re = re.compile('<td.+?bgcolor="#fdfddf"><a href="(.+?)">')
    downloadlink = downloadlink_re.findall(content)   
    if downloadlink:
        downloadlink = downloadlink[0]
    else:
        downloadlink = None
    return downloadlink


# ------------我是华丽的分割线-----------------------------

def save_movie(con):
    movie = {}
    movie["title"] = get_title(con)
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
    return movie


def get_info( url, movielist):
    """得到所有信息"""
    response = urllib2.urlopen(url)
    content = response.read()
    content = content.decode('gbk','ignore')
    time.sleep(1)
    movie =save_movie(content)
    if not movie['title']:
        movielist.append(movie)
    return movielist



def run( url,movielist):
    response = urllib2.urlopen(url)
    content = response.read()
    ft = re.compile('<a href="(.*?)" class="ulink">')
    urls = ft.findall(content)
    for item in urls:
        new_url = 'http://www.ygdy8.net' + item
        movielist = (get_info(new_url,movielist))
    return movielist

def get_page_number():
    url = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
    response = urllib2.urlopen(url)
    content = response.read()
    url_re = re.compile(u'共(\d*?)页')
    number = url_re.findall(content.decode('gbk','ignore'))
    return int(number[0])


if __name__ == '__main__':
    
    page_number = get_page_number()
    print '共',page_number,'页'
    movielist = []
    for i in range(page_number):
        url = 'http://www.ygdy8.net/html/gndy/dyzz/list_23_'+str(i+1) + '.html'
        print "第 ",i+1," 页正在下载"
        movielist = run(url, movielist)
        

