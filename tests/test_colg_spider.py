from scrapy.selector import Selector
from scrapy.http import TextResponse
from voc_crawler.spiders import colg_spider, ColgSpider


class TestColgSpider():

    def test_get_comment_page_no(self):
        assert colg_spider.get_comment_page_no('http://bbs.colg.cn/thread-1231234-2-1.html') == 2
        assert colg_spider.get_comment_page_no('http://bbs.colg.cn/thread-1234123412-4-1.html') == 4
        assert colg_spider.get_comment_page_no('http://bbs.colg.cn/thread-7313182-4-10.html') == 4
        assert colg_spider.get_comment_page_no('http://bbs.colg.cn/thread-7317588-12-2.html') == 12
    
    def test_replace_comment_page_no(self):
        assert colg_spider.replace_comment_page_no('thread-12345-11-123.html', 10) == 'thread-12345-10-123.html'
        assert colg_spider.replace_comment_page_no('thread-23452345-12-123.html', 8) == 'thread-23452345-8-123.html'
        assert colg_spider.replace_comment_page_no('thread-4623455-3-123.html', 1) == 'thread-4623455-1-123.html'
    
    def test_get_commentlistpage_urls_near_endof_lastpage(self):
        spider = ColgSpider()
        spider.custom_settings['CRAWLE_RANGE_COMMENT_PAGE'] = 2
        actual = list(colg_spider.get_commentlistpage_urls_near_endof_lastpage('thread-4623455-3-123.html', spider))
        assert actual == ['thread-4623455-3-123.html', 'thread-4623455-2-123.html']

        spider.custom_settings['CRAWLE_RANGE_COMMENT_PAGE'] = 3
        actual2 = list(colg_spider.get_commentlistpage_urls_near_endof_lastpage('thread-4623455-3-123.html', spider))
        assert actual2 == ['thread-4623455-3-123.html', 'thread-4623455-2-123.html', 'thread-4623455-1-123.html']
    