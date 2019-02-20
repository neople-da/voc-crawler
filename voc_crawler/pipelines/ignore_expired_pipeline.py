from datetime import datetime

from scrapy.exceptions import DropItem

class IgnoreExpiredPipeline(object):
    def __init__(self, expireDays):
        self.expireDays = expireDays

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            expireDays = crawler.settings.get('EXPIRE_DAYS')
        )

    def process_item(self, item, spider):
        isArticle = item['type'] == 'article'
        if self.isExpired(isArticle, item['writeDate']):
            raise DropItem("Expired item found: %s" % item)
        return item
    
    def isExpired(self, isArticle, writeDate):
        dt = datetime.strptime(writeDate, '%Y-%m-%d %H:%M')
        now = datetime.now()
        timedelta = now - dt
        return timedelta.days > self.expireDays
