#coding:utf-8

import MySQLdb

def create():
    '''创建数据库'''
    try:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',charset='utf8')
        cur = conn.cursor()
        
        cur.execute('drop database dyttmovie')
        
        cur.execute("create database if not exists dyttmovie charset='utf8'")
        conn.select_db('dyttmovie')
        #建表

        cur.execute('''create table movies (
            id int ,
            title varchar(100) not null,
            publishdate varchar(50),
            imageurl varchar(100),
            subtitles varchar(30),
            fileformat varchar(30),
            width varchar(20),
            height varchar(20),
            size varchar(100),
            duration varchar(50),
            director varchar(50)
            )''')

        # chname
        cur.execute('''create table chnames(
            id int,
            chname varchar(100)
            )''')
        cur.execute('''create table movie_chnames(
            movie_id int,
            chname_id int
            )''')

        #name
        cur.execute('''create table names(
            id int,
            name varchar(100)
            )''')
        cur.execute('''create table movie_names(
            movie_id int,
            name_id int
            )''')

        #type
        cur.execute('''create table types(
            id int,
            type varchar(20)
            )''')
        cur.execute('''create table movie_types(
            movie_id int,
            type_id int
            )''')

        #language
        cur.execute('''create table languages(
            id int,
            language varchar(20)
            )''')
        cur.execute('''create table movie_languages(
            movie_id int,
            language_id int
            )''')

        #actors
        cur.execute('''create table actors(
            id int,
            actor varchar(50)
            )''')
        cur.execute('''create table movie_actors(
            movie_id int,
            actor_id int
            )''')

        #introduce
        cur.execute('''create table introduces(
            id int,
            introduce varchar(10000)
            )''')
        cur.execute('''create table movie_introduces(
            movie_id int,
            introduce_id int
            )''')
        
        #introduceimageurl
        cur.execute('''create table iiurls(
            id int,
            iirul varchar(100)
            )''')
        cur.execute('''create table movie_iiurls(
            movie_id int,
            iiurl_id int
            )''')

        #downloadurl
        cur.execute('''create table durls(
            id int,
            durl varchar(100)
            )''')
        cur.execute('''create table movie_durls(
            movie_id int,
            durl_id int
            )''')
        cur.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d : %s"%(e.args[0],e.args[1])
        
        
if __name__ == '__main__':
    create()
