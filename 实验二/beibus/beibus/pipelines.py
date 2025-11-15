# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import pymysql
from beibus import settings
class MysqlPipeline(object):
    def __init__(self):
        self.host = settings.DB_HOST
        self.user = settings.DB_USER
        self.pwd = settings.DB_PWD
        self.db = settings.DB
        self.charset = settings.DB_CHARSET
        self.connect()

    def connect(self):
        self.conn = pymysql.connect(host=self.host,
                                    user=self.user,
                                    password=self.pwd,
                                    db=self.db,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()

    def process_item(self, item, spider):
        sql = 'INSERT INTO businfo (line_name, line_type, run_time, mileage, ticket, company, update_last, wang_info, fan_info) VALUES ("%s","%s","%s","%s","%s","%s","%s","%s","%s")'%(
        item['line_name'], item['line_type'], item['run_time'],
        item['mileage'], item['ticket'], item['company'], item['update_last'], item['wang_info'], item['fan_info'])
        # 执行SQL语句
        self.cursor.execute(sql)
        self.conn.commit()
        return item


