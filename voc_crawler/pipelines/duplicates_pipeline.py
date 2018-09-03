from redis.sentinel import Sentinel
from scrapy.exceptions import DropItem
from scrapy.selector import Selector

class DuplicatesPipeline(object):
    def __init__(self, redisHost, redisPort, redisServiceName):
        self.redisHost = redisHost
        self.redisPort = redisPort
        self.redisServiceName = redisServiceName
        # self.sentinel = Sentinel([('localhost', 6000)], socket_timeout=0.1)
        # self.master = self.sentinel.master_for('Common', socket_timeout=0.1)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redisHost = crawler.settings.get('REDIS_HOST'),
            redisPort = crawler.settings.get('REDIS_PORT'),
            redisServiceName=crawler.settings.get('REDIS_SERVICE_NAME')
        )

    def open_spider(self, spider):
        self.sentinel = Sentinel([(self.redisHost, self.redisPort)], socket_timeout=0.1)
        self.client = self.sentinel.master_for(self.redisServiceName, socket_timeout=0.1)

    # def close_spider(self, spider):
    #     self.client.close()
        
    def process_item(self, item, spider):
        isComment = item['type'] != 'article'

        # if isComment:
        #     if self.client.getbit('colg:article', item['articleId']) == False:
        #         raise DropItem('parent article not found: %s' % item)

        historyRedis = 'colg:comment' if isComment else 'colg:article'

        if self.client.getbit(historyRedis, item['id']) == True:
            raise DropItem("Duplicate item found: %s" % item)
        else:
            self.client.setbit(historyRedis, item['id'], 1)
            return item
