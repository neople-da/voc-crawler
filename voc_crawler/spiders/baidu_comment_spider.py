
import json
import urllib.parse as urlparse

from scrapy import Spider
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector

from .baidu_spider_settings import BAIDU_HOST, VOC_GAME_TYPE, VOC_SITE_ID, VOC_BOARD_ID, START_URL_FORMAT, UTC_OFFSET, CRAWLE_RANGE_COMMENT_PAGE, MAX_PAGE

class BaiduCommentSpider(Spider):
    HOST = BAIDU_HOST
    name = 'baidu_comment'
    urls = [START_URL_FORMAT.format(n * 50) for n in range(0,MAX_PAGE)]
    start_urls = urls
    custom_settings = {
        'UTC_OFFSET': UTC_OFFSET,
        'CRAWLE_RANGE_COMMENT_PAGE': CRAWLE_RANGE_COMMENT_PAGE,
        'VOC_GAME_TYPE': 'CDNF',
        'VOC_SITE_ID': VOC_SITE_ID,
        'VOC_BOARD_ID': VOC_BOARD_ID
    }

    def parse(self, response: HtmlResponse):
        articleLinks = get_article_links(response)

        for articleLink in articleLinks:
            yield response.follow(articleLink, parse_comment)

def get_article_links(response: HtmlResponse):
    return response.css('.threadlist_title a.j_th_tit')

def get_comment_page_links(response: HtmlResponse):
    lastUrl = response.css('.pb_list_pager > a:last-child').xpath('@href').extract_first()
    if lastUrl != None:
        parsedUrl = urlparse.urlparse(lastUrl)
        qsDic = urlparse.parse_qs(parsedUrl.query)
        if 'pn' in qsDic:
            lastPageNo = int(qsDic['pn'][0])
            minPageNo = 1 if (lastPageNo - CRAWLE_RANGE_COMMENT_PAGE) <= 0 else lastPageNo - CRAWLE_RANGE_COMMENT_PAGE
            for pageNo in range(lastPageNo, minPageNo, -1):
                yield f'{response.url}?pn={pageNo}'
        else:
            return
    
def parse_comment(response: HtmlResponse):
    commentDivs = response.css('#j_p_postlist > div.l_post')
    isFirstPage = get_comment_page_no(response.request.url) == 1
    if isFirstPage:
        del commentDivs[0]
        commentPageLinks = get_comment_page_links(response)
        for commentPage in commentPageLinks:
            yield response.follow(commentPage, parse_comment)
    
    for div in commentDivs:
        dataAttr = div.xpath('@data-field').extract_first()
        x = json.loads(dataAttr)
        yield {
            'boardId': 'baidu:comment',
            'type': 'comment',
            'url': response.request.url,
            'id': x['content']['post_id'],
            'content': x['content']['content'],
            'writeDate': parse_comment_writedate(div),
            'writer': x['author']['user_name'],
            'articleId': x['content']['thread_id']
        }

def get_comment_page_no(url):
    parsedUrl = urlparse.urlparse(url)
    qsDic = urlparse.parse_qs(parsedUrl.query)
    if 'pn' in qsDic:
        return int(qsDic['pn'][0])
    else:
        return 1 

def parse_comment_writedate(selector: Selector):
    return selector.css('.post-tail-wrap > span:last-child::text').extract_first().strip()