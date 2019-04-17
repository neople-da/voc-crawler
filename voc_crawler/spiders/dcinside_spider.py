import re
from scrapy import Spider
from scrapy.exceptions import DropItem
from scrapy.http.response.html import HtmlResponse

DC_HOST = 'https://gall.dcinside.com'
# https://gall.dcinside.com/board/view/?id=d_fighter_new1&no=8961148&page=1
# https://gall.dcinside.com/board/lists/?id=d_fighter_new1&page=2
DC_GALL_NAME = 'd_fighter_new1'
REGEX_ARTICLEID = re.compile(DC_HOST + r'/board/view/\?id=d_fighter_new1&no=(\d*)')
    # https://gall.dcinside.com/board/view/\?id=d_fighter_new1&no=(\d*)
MAX_PAGE = 5


VOC_GAME_TYPE = 'KDNF'
VOC_SITE_ID = 5
VOC_BOARD_ID = 1

class DcinsideSpider(Spider):
    name = 'dcinside'
    urls = [f'{DC_HOST}/board/lists/?id={DC_GALL_NAME}&page={n}' for n in range(1,MAX_PAGE+1)]
    start_urls = urls

    custom_settings = {
        'VOC_GAME_TYPE': VOC_GAME_TYPE,
        'VOC_SITE_ID': VOC_SITE_ID,
        'VOC_BOARD_ID': VOC_BOARD_ID,
        'UTC_OFFSET': '+0900',
        'DOWNLOAD_DELAY': 1,
    }

    def parse(self, response: HtmlResponse):
        articleLinks = get_article_links(response)
        for articleLink in articleLinks:
            yield response.follow(articleLink, parse_article)

def get_article_links(response: HtmlResponse):
    return response.css('tr.ub-content td.gall_tit a:not(.reply_numbox)')

def parse_article(response: HtmlResponse):
    yield {
        'boardId': 'dc:kdnf',
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
    return response.css('.title_subject::text').extract_first().strip()

def parse_article_content(response: HtmlResponse):
    return ''.join(response.css('.writing_view_box')[0].xpath('node()').extract())

def parse_article_writedate(response: HtmlResponse):
    return response.css('span.gall_date').xpath('@title').extract_first().strip()[:-3]

def parse_article_writer(response: HtmlResponse):
    return response.css('.gallview_head .gall_writer').xpath('@data-nick').extract_first().strip()