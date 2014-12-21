
创建数据库  
运行 download/create-db.py 

可以考虑注释或取消注释  

```
drop database if exists dyttmovie
```

因为在python运行的时候，`create database if not exists dyttmovie` 等如果存在`dyttmovie`数据库，就会报错。  

电影天堂爬虫数据处理.  
download/dytt-movie-db.py  

