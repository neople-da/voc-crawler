import math
from datetime import datetime, timedelta

from redis.sentinel import Sentinel

from .settings import REDIS_HOST, REDIS_PORT, REDIS_SERVICE_NAME

class HistoryRepository(object):
    sentinel = Sentinel([(REDIS_HOST, REDIS_PORT)], socket_timeout=0.2)
    client = sentinel.master_for(REDIS_SERVICE_NAME, socket_timeout=0.2)
    REDIS_BIT_MAX = 4294967296 - 1

    @classmethod
    def write(cls, item, expireDays):
        # (legacy_key, legacy_offset) = cls.get_cropped_key_and_offset(item['boardId'], item['id'])
        # cls.client.setbit(legacy_key, legacy_offset, 1)

        dt = datetime.strptime(item['writeDate'], '%Y-%m-%d %H:%M')
        weekNumber = dt.isocalendar()[1]
        key = f"{item['boardId']}:{weekNumber}"
        member = item['id']
        cls.client.sadd(key, member)
        cls.client.expireat(key, dt + timedelta(days=expireDays))

    @classmethod
    def erase(cls, item):
        (legacy_key, legacy_offset) = cls.get_cropped_key_and_offset(item['boardId'], item['id'])
        cls.client.setbit(legacy_key, legacy_offset, 0)

        dt = datetime.strptime(item['writeDate'], '%Y-%m-%d %H:%M')
        weekNumber = dt.isocalendar()[1]
        key = f"{item['boardId']}:{weekNumber}"
        member = item['id']
        cls.client.srem(key, member)

    @classmethod
    def exist(cls, item) -> bool:
        legacy_key, legacy_offset = cls.get_cropped_key_and_offset(item['boardId'], item['id'])
        if cls.client.getbit(legacy_key, legacy_offset) == True:
            return True

        weekNumber = datetime.strptime(item['writeDate'], '%Y-%m-%d %H:%M').isocalendar()[1]
        key = f"{item['boardId']}:{weekNumber}"
        member = item['id']
        return cls.client.sismember(key, member) == True

    # def getCurrentMonthKey(self, writeDate: datetime):
    #     remainder = writeDate.month % 3
    #     quotient = math.floor(writeDate.month / 3)
    #     return 3 * quotient + (-2 if remainder == 0 else 1)
    
    # def getCurrentWeekKey(self, writeDate: datetime):
    #     weekNumber = writeDate.isocalendar()[1]
    #     isEven = weekNumber % 2 == 0
    #     return weekNumber - 1 if isEven else weekNumber
    
    # @classmethod
    # def article_exist(cls, item) -> bool:
    #     key = 'cd:c' if item['site'] == 'colg' else item['site'] + ':article'
    #     offset = item['articleId']
    #     key, offset = cls.get_cropped_key_and_offset(key, offset)
    #     return cls.client.getbit(key, offset) == True

    @classmethod
    def get_cropped_key_and_offset(cls, key, offset) -> (int, int):
        resultKey = key
        resultOffset = offset

        if offset > cls.REDIS_BIT_MAX:
            resultKey = key + ':' + str(math.floor(offset / 10000000))
            resultOffset = offset % 10000000
        return resultKey, resultOffset