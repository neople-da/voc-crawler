import re
import urllib.parse as urlparse
import json
from collections import namedtuple

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector

from .baidu_spider_settings import BAIDU_HOST, VOC_GAME_TYPE, VOC_SITE_ID, VOC_BOARD_ID, START_URL_FORMAT, UTC_OFFSET, CRAWLE_RANGE_COMMENT_PAGE, MAX_PAGE

class BaiduSpider(Spider):
    HOST = BAIDU_HOST
    name = 'baidu'
    urls = [START_URL_FORMAT.format(n * 50) for n in range(0,MAX_PAGE)]
    start_urls = urls
    custom_settings = {
        'UTC_OFFSET': UTC_OFFSET,
        'CRAWLE_RANGE_COMMENT_PAGE': CRAWLE_RANGE_COMMENT_PAGE,
        'VOC_GAME_TYPE': VOC_GAME_TYPE,
        'VOC_SITE_ID': VOC_SITE_ID,
        'VOC_BOARD_ID': VOC_BOARD_ID
    }

    def parse(self, response: HtmlResponse):
        articleLinks = get_article_links(response)

        for articleLink in articleLinks:
            yield response.follow(articleLink, parse_article)

REGEX_ARTICLEID = re.compile(BAIDU_HOST + r'/p/(\d*)')

def get_article_links(response: HtmlResponse):
    return response.css('.threadlist_title a.j_th_tit')

def parse_article(response: HtmlResponse):
    yield {
        'boardId': 'baidu:article',
        'type': 'article',
        'url': response.url,
        'id': parse_articleid(response.request.url),
        'title': parse_article_title(response),
        'content': parse_article_content(response),
        'writeDate': parse_article_writedate(response),
        'writer': parse_article_writer(response)
    }

def parse_articleid(url):
    return int(REGEX_ARTICLEID.findall(url)[0])

def parse_article_title(response: HtmlResponse):
    return response.css('.core_title_txt::text').extract_first().strip()

def parse_article_content(response: HtmlResponse):    
    return ''.join(response.css('.d_post_content')[0].xpath('node()').extract()).strip()

def parse_article_writedate(response: HtmlResponse):
    return response.css('.post-tail-wrap span:last-child::text').extract_first().strip()

def parse_article_writer(response: HtmlResponse):
    return response.css('.p_author_name::text').extract_first().strip()