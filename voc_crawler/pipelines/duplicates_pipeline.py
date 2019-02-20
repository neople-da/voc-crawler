from scrapy.exceptions import DropItem
from scrapy.selector import Selector

from voc_crawler.history_repository import HistoryRepository

class DuplicatesPipeline(object):

    def __init__(self, expireDays):
        self.expireDays = expireDays

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            expireDays = crawler.settings.get('EXPIRE_DAYS')
        )

    def process_item(self, item, spider):
        
        if HistoryRepository.exist(item):
            raise DropItem("Duplicate item found: %s" % item)
        HistoryRepository.write(item, self.expireDays)
        return item
