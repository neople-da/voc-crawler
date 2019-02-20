import re

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse

from .inven_base import INVEN_HOST, get_article_links, parse_article_base

MAX_PAGE = 3
INVEN_GAME_NAME = 'maple'
INVEN_BOARD_ID = 2299
VOC_GAME_TYPE = 'Other'
VOC_SITE_ID = 2
VOC_BOARD_ID = 20

class InvenLolSubcultureSpider(Spider):
    name = 'maple_free'
    urls = [f'{INVEN_HOST}{INVEN_GAME_NAME}/{INVEN_BOARD_ID}?sort=PID&p={n}' for n in range(1,MAX_PAGE+1)]
    start_urls = urls

    custom_settings = {
        'VOC_GAME_TYPE': VOC_GAME_TYPE,
        'VOC_SITE_ID': VOC_SITE_ID,
        'VOC_BOARD_ID': VOC_BOARD_ID,
        'UTC_OFFSET': '+0900',
    }
    
    def parse(self, response: HtmlResponse):
        articleLinks = get_article_links(response)
        for articleLink in articleLinks:
            yield response.follow(articleLink, self.parse_article)

    def parse_article(self, response: HtmlResponse):
        return parse_article_base(INVEN_GAME_NAME, INVEN_BOARD_ID, response)