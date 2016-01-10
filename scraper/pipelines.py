import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class JournalPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db['journals']

    def process_item(self, item, spider):
        if spider.name != "journal":
            return item

        for data in item:
            if not data:
                raise DropItem("Missing {0}!".format(data))

        self.collection.update({'title': item['title']}, dict(item), upsert=True)
        log.msg("Journal added to db", level=log.DEBUG, spider=spider)
        return item


class ArticlePipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.collection = db['articles']

    def process_item(self, item, spider):
        if spider.name != "article":
            return item

        for data in item:
            if not data:
                raise DropItem("Missing {0}!".format(data))
        # check to see if article already exists and add if it doesn't
        if self.collection.find_one({'title': item['title']}):
            return item
        else:
            self.collection.update({'url': item['url']}, dict(item), upsert=True)
            log.msg("Article added to db", level=log.DEBUG, spider=spider)
            return item
