import datetime as dt
from voc_crawler.pipelines import IgnoreExpiredPipeline

class TestIgnoreExpiredPipeline():

    def test_isExpired(self):
        expiredays = 10
        pipe = IgnoreExpiredPipeline(expiredays, expiredays)

        assert pipe.isExpired(True, (dt.datetime.now() - dt.timedelta(days=expiredays - 1)).strftime('%Y-%m-%d %H:%M')) == False
        assert pipe.isExpired(True, (dt.datetime.now() - dt.timedelta(days=expiredays)).strftime('%Y-%m-%d %H:%M')) == False
        assert pipe.isExpired(True, (dt.datetime.now() - dt.timedelta(days=expiredays + 1)).strftime('%Y-%m-%d %H:%M')) == True