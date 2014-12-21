#coding:utf-8

import MySQLdb

def create():
    '''创建数据库'''
    try:
        conn = MySQLdb.connect(host='localhost',user='root',passwd='123456',charset='utf8')
        cur = conn.cursor()
        
        cur.execute('drop database if exists dyttmovie')
        
        cur.execute("create database if not exists dyttmovie charset='utf8'")
        conn.select_db('dyttmovie')
        #建表

        cur.execute('''create table movies (
            id int ,
            title varchar(100) not null,
            publishdate varchar(50),
            imageurl varchar(500),
            type varchar(100),
            language varchar(100),
            subtitles varchar(30),
            fileformat varchar(30),
            width varchar(20),
            height varchar(20),
            size varchar(100),
            duration varchar(100),
            director varchar(100),
            introduceimageurl varchar(100),
            downloadlink varchar(200)
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
            name varchar(500)
            )''')
        cur.execute('''create table movie_names(
            movie_id int,
            name_id int
            )''')

        #actors
        cur.execute('''create table actors(
            id int,
            actor varchar(500)
            )''')
        cur.execute('''create table movie_actors(
            movie_id int,
            actor_id int
            )''')

        #introduce
        cur.execute('''create table introduces(
            id int,
            introduce varchar(4000)
            )''')
        cur.execute('''create table movie_introduces(
            movie_id int,
            introduce_id int
            )''')

        cur.close()
    except MySQLdb.Error,e:
        print "Mysql Error %d : %s"%(e.args[0],e.args[1])
        
        
if __name__ == '__main__':
    create()
