from redis.sentinel import Sentinel
from .settings import REDIS_HOST, REDIS_PORT, REDIS_SERVICE_NAME

class HistoryRepository(object):
    sentinel = Sentinel([(REDIS_HOST, REDIS_PORT)], socket_timeout=0.1)
    client = sentinel.master_for(REDIS_SERVICE_NAME, socket_timeout=0.1)

    @classmethod
    def write(cls, key, isComment= False):
        historyRedis = 'colg:comment' if isComment else 'colg:article'
        cls.client.setbit(historyRedis, key, 1)

    @classmethod
    def erase(cls, key, isComment= False):
        historyRedis = 'colg:comment' if isComment else 'colg:article'
        cls.client.setbit(historyRedis, key, 0)

    @classmethod
    def exist(cls, key, isComment= False) -> bool:
        historyRedis = 'colg:comment' if isComment else 'colg:article'
        return cls.client.getbit(historyRedis, key) == True