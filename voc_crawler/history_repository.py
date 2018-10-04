import math
from redis.sentinel import Sentinel
from .settings import REDIS_HOST, REDIS_PORT, REDIS_SERVICE_NAME

class HistoryRepository(object):
    sentinel = Sentinel([(REDIS_HOST, REDIS_PORT)], socket_timeout=0.2)
    client = sentinel.master_for(REDIS_SERVICE_NAME, socket_timeout=0.2)
    REDIS_BIT_MAX = 4294967296 - 1

    @classmethod
    def write(cls, item):
        (key, offset) = cls.get_cropped_key_and_offset(item['site'] + ':' + item['type'], item['id'])
        cls.client.setbit(key, offset, 1)

    @classmethod
    def erase(cls, item):
        (key, offset) = cls.get_cropped_key_and_offset(item['site'] + ':' + item['type'], item['id'])
        cls.client.setbit(key, offset, 0)

    @classmethod
    def exist(cls, item) -> bool:
        key, offset = cls.get_cropped_key_and_offset(item['site'] + ':' + item['type'], item['id'])
        return cls.client.getbit(key, offset) == True
    
    @classmethod
    def article_exist(cls, item) -> bool:
        key = 'cd:c' if item['site'] == 'colg' else item['site'] + ':article'
        offset = item['articleId']
        key, offset = cls.get_cropped_key_and_offset(key, offset)
        return cls.client.getbit(key, offset) == True

    @classmethod
    def get_cropped_key_and_offset(cls, key, offset) -> (int, int):
        resultKey = key
        resultOffset = offset

        if offset > cls.REDIS_BIT_MAX:
            resultKey = key + ':' + str(math.floor(offset / 10000000))
            resultOffset = offset % 10000000
        return resultKey, resultOffset