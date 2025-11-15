# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

from itemadapter import ItemAdapter
import json
import pymysql


class ScrapypoemPipeline:
    def __init__(self):
        # 打开文件
        self.file = open('poems.txt', 'w', encoding='utf-8')
        # # 连接MySQL数据库
        # self.connect = pymysql.connect(
        #     host='localhost',
        #     port=3306,
        #     user='root',
        #     passwd='123456',  # 设置成用户自己的数据库密码
        #     db='poems',
        #     charset='utf8'
        # )
        # self.cursor = self.connect.cursor()
        # # 创建数据表
        # self.cursor.execute(
        #     'DROP TABLE IF EXISTS beautifulsentence;'
        # )
        # self.cursor.execute(
        #     'CREATE TABLE beautifulsentence(`source` varchar(255) NOT NULL,`sentence`varchar(255) NOT NULL,'
        #     '`content` text NOT NULL,`url` varchar(255) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
        # )
        # self.connect.commit()

    def process_item(self, item, spider):
        # 读取item中的数据
        line = json.dumps(dict(item), ensure_ascii=False) + '\n'
        # 写入文件
        self.file.write(line)
        # # 写入数据库
        # self.cursor.execute(
        #     'INSERT INTO beautifulsentence(source,sentence,content,url) VALUES ("{}","{}","{}","{}")'.format(
        #         item['source'], item['sentence'], item['content'], item['url']))
        # self.connect.commit()
        return item

    def close_spider(self, spider):
        pass
        self.file.close()
        # 关闭数据库连接
        # self.cursor.close()
        # self.connect.close()
