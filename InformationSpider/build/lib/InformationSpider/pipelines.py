# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.pipelines.images import ImagesPipeline
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class InformationspiderPipeline(object):
    def process_item(self, item, spider):
        return item


#自定义图片下载处理
class MovieImagePipeline(ImagesPipeline):
    def item_completed(self, results, item, info):
        if "image_urls" in item:
            for ok, value in results:
                image_file_path = value["path"]
            item["image_path"] = image_file_path
        return item



#异步mysql写入
class MysqlTwistedpipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host = settings['MYSQL_HOST'],
            database = settings['MYSQL_DBNAME'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True,
        )
        # 连接池ConnectionPool
        # def __init__(self, dbapiName, *connargs, **connkw):
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        # 此处相当于实例化pipeline, 要在init中接收。
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行：参数1：我们自定义一个函数,里面可以写我们的插入逻辑
        query = self.dbpool.runInteraction(self.do_insert, item)
        # 添加自己的处理异常的函数
        query.addErrback(self.handle_error, item, spider)



    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        insert_sql, params = item.get_insert_sql()
        cursor.execute(insert_sql, params)

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        print (failure)


