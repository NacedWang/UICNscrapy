# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import redis


class UicnPipeline(object):

    def __init__(self):
        # redis链接
        self.redisConn = redis.Redis(host='127.0.0.1', port=6379)
        self.redisPrefix = "uicn:experience:"

    def open_spider(self, spider):
        # 爬虫开启的时候调用，只调用一次
        print('爬虫文件开始执行', spider.name)

    def process_item(self, item, spider):
        print('管道文件我来了')
        try:
            res = self.redisConn.hmset(self.redisPrefix + item['id'], item)
        except Exception as err:
            print(err)
        return item

    def close_spider(self, spider):
        # 爬虫结束的时候会调用，只调用一次
        print('爬虫文件结束执行', spider.name)
        # 关闭游标和关闭连接
        self.redisConn.close()
