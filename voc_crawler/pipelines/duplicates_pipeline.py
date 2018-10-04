from scrapy.exceptions import DropItem
from scrapy.selector import Selector

from voc_crawler.history_repository import HistoryRepository

class DuplicatesPipeline(object):

    def process_item(self, item, spider):
        if HistoryRepository.exist(item):
            raise DropItem("Duplicate item found: %s" % item)
        HistoryRepository.write(item)
        return item
