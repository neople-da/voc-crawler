from scrapy.selector import Selector
from scrapy.http import TextResponse
from voc_crawler.spiders import colg_spider, ColgSpider


class TestColgSpider():

    def test_get_comment_page_no(self):
        assert colg_spider.get_comment_page_no('http://bbs.colg.cn/thread-1231234-2-1.html') == 2
        assert colg_spider.get_comment_page_no('http://bbs.colg.cn/thread-1234123412-4-1.html') == 4
        assert colg_spider.get_comment_page_no('http://bbs.colg.cn/thread-123423-1-1.html') == 1
    
    