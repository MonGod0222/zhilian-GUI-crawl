# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
import pymongo


class MysqlPipeline(object):
    
    def __init__(self, host, database, user, password, port, table):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.table = table

    @classmethod
    def from_crawler(cls, crawler):
        if int(crawler.settings.get('set_mysql')) != 1:
            return None
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            user=crawler.settings.get('set_user'),
            password=crawler.settings.get('set_password'),
            port=crawler.settings.get('MYSQL_PORT'),
            table=crawler.settings.get('COLLECTION')
        )

    def open_spider(self, spider):
        
        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password,
                                  port=self.port)
   
        self.cursor = self.db.cursor()

        # 创建zhilian数据库
        sql_d = 'CREATE DATABASE IF NOT EXISTS zhilian'
        self.cursor.execute(sql_d)

        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()
        # 创建表
        sql_t = 'CREATE TABLE IF NOT EXISTS {} '.format(
            self.table) + '(url VARCHAR(512) NOT NULL, keyword VARCHAR(128) NOT NULL, position VARCHAR(128) NOT NULL, monthly_pay_range VARCHAR(128) NOT NULL,\
        monthly_pay_min VARCHAR(20) NOT NULL,monthly_pay_max VARCHAR(20) NOT NULL,company_name VARCHAR(128) NOT NULL,site VARCHAR(128) NOT NULL,\
        experience VARCHAR(128) NOT NULL,education_background VARCHAR(128) NOT NULL,number_of_people VARCHAR(128) NOT NULL,bright_spots VARCHAR(255) NOT NULL,position_information VARCHAR(2047) ,company_profile VARCHAR(2047))'
        self.cursor.execute(sql_t)
    

    def close_spider(self, spider):
        self.db.close()
        

    def process_item(self, item, spider):

        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))

        self.db = pymysql.connect(host=self.host, user=self.user, password=self.password, db=self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

        sql = 'insert into %s (%s) values (%s)' % (self.table, keys, values)
        sql_find = 'SELECT * FROM {} WHERE url="{}"'.format(
            self.table, item['url'])
        re_find = self.cursor.execute(sql_find)
        if re_find == 0:
            self.cursor.execute(sql, tuple(data.values()))
            self.db.commit()

        return item


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db, mongo_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.collection = mongo_collection

    @classmethod
    def from_crawler(cls, crawler):

        if int(crawler.settings.get('set_mongo')) != 1:
            return None
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB'),
            mongo_collection=crawler.settings.get('COLLECTION')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def process_item(self, item, spider):

        name = self.collection
        if not self.db[name].find_one({'position': item['url']}):
            self.db[name].insert(dict(item))
        return item

    def close_spider(self, spider):
        self.client.close()
