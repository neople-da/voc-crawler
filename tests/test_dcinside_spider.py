#-*-coding: utf-8
import os
from scrapy.selector import Selector
# from scrapy.http import TextResponse
from voc_crawler.spiders import dcinside_spider
from scrapy.http import HtmlResponse, Request

class TestDcinsideSpider():
    def test_parse_articleid(self):
        assert dcinside_spider.parse_articleid('https://gall.dcinside.com/board/view/?id=d_fighter_new1&no=8961128&page=2') == 8961128
        assert dcinside_spider.parse_articleid('https://gall.dcinside.com/board/view/?id=d_fighter_new1&no=8961127&page=2') == 8961127
        assert dcinside_spider.parse_articleid('https://gall.dcinside.com/board/view/?id=d_fighter_new1&no=8961126&page=2') == 8961126
    
    def test_parse_article_title(self):
        file_path = "D:\\OneDrive - 네오플\\12.VOC\\20190416 DC크롤링\\test article page.html"
        response = self.fake_response_from_file(file_path, url='https://gall.dcinside.com/board/view/?id=d_fighter_new1&no=8961416&page=1')
        assert dcinside_spider.parse_article_title(response) == '걍 시너지 문제는 인구 많은 퓨딜 시너지화 하면 해결댐'
    
    def test_parse_article_content(self):
        file_path = "D:\\OneDrive - 네오플\\12.VOC\\20190416 DC크롤링\\test article page.html"
        response = self.fake_response_from_file(file_path, url='https://gall.dcinside.com/board/view/?id=d_fighter_new1&no=8961416&page=1')

        contents = ('<div id="zzbang_div" style=""></div>'
        '<pre></pre>'
        '<div style="overflow:hidden;">'
        '<p>까마귀</p>'
        '<p><br></p>'
        '<p>버서커</p>'
        '<p><br></p>'
        '<p>소마</p>'
        '<p><br></p>'
        '<p>배메&nbsp;</p>'
        '<p><br></p>'
        '<p>이런 애들 다 시너지화 시키면 시너지난 해결</p>'
        '<p><br></p>'
        '<p><br></p>'
        '<p style="text-align: left;"><img src="https://dcimg6.dcinside.co.kr/viewimage.php?id=2982d62fe2da2ca37c80d8b00180&amp;no=24b0d769e1d32ca73fee83fa11d02831be17f6b16442b2da382c1b3eac2ce2b3a4defcfead7286a8095b26b00fff29398d1a2996118bbf42fa83fd8d447d34b036d5248788" class="txc-image" style="clear:none;float:none;"></p>'
        '<p><br></p>'
        '<p><br></p>'
        '</div>')
        assert dcinside_spider.parse_article_content(response).replace('\t', '').replace('\n', '') == contents.replace('\t', '').replace('\n', '')
    
    def test_parse_article_writedate(self):
        file_path = "D:\\OneDrive - 네오플\\12.VOC\\20190416 DC크롤링\\test article page.html"
        response = self.fake_response_from_file(file_path, url='https://gall.dcinside.com/board/view/?id=d_fighter_new1&no=8961416&page=1')
        assert dcinside_spider.parse_article_writedate(response) == '2019-04-16 14:06'

    def test_parse_article_writer(self):
        file_path = "D:\\OneDrive - 네오플\\12.VOC\\20190416 DC크롤링\\test article page.html"
        response = self.fake_response_from_file(file_path, url='https://gall.dcinside.com/board/view/?id=d_fighter_new1&no=8961416&page=1')
        assert dcinside_spider.parse_article_writer(response) == 'ㅇㅇ'

    def fake_response_from_file(self, file_name, url=None):
        """
        Create a Scrapy fake HTTP response from a HTML file
        @param file_name: The relative filename from the responses directory,
                        but absolute paths are also accepted.
        @param url: The URL of the response.
        returns: A scrapy HTTP response which can be used for unittesting.
        """
        if not url:
            url = 'http://www.example.com'

        request = Request(url=url)
        if not file_name[0] == '/':
            responses_dir = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(responses_dir, file_name)
        else:
            file_path = file_name

        file_content = open(file_path, 'r', encoding='utf8').read()

        response = HtmlResponse(url=url,
            request=request,
            body=str.encode(file_content), encoding='utf-8')
        # response.encoding = 'utf-8'
        return response