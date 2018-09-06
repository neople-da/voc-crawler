import re
from urllib.parse import urlparse

from scrapy import Spider
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import Join
from scrapy.exceptions import DropItem
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector

from .colg_spider_settings import COLG_HOST, START_URL_FORMAT, UTC_OFFSET, CRAWLE_RANGE_COMMENT_PAGE, MAX_PAGE

class ColgSpider(Spider):
    HOST = COLG_HOST
    name = 'colg'
    urls = [START_URL_FORMAT.format(n) for n in range(1,MAX_PAGE+1)]
    start_urls = urls

    custom_settings = {
        'UTC_OFFSET': UTC_OFFSET,
        'CRAWLE_RANGE_COMMENT_PAGE': CRAWLE_RANGE_COMMENT_PAGE
    }

    def parse(self, response: HtmlResponse):
        
        articleLinks = get_article_links(response)
        # for articleLink in articleLinks:
        #     yield response.follow(articleLink, parse_article)

        #comments in first page
        for articleLink in articleLinks:
            yield response.follow(articleLink, parse_comment) 

        commentLinks = get_comment_links(response, self)
        for commentLink in commentLinks:
            yield response.follow(commentLink, parse_comment)

REGEX_ARTICLEID = re.compile(COLG_HOST + r'/thread-(\d*)-(\d*)-(\d*).html')
REGEX_COMMENTPAGE_LINK = re.compile(r'thread-(\d*)-(\d*)-(\d*).html')
REGEX_COMMENT_ID = re.compile(r'post_(\d*)')

def get_article_links(response: HtmlResponse):
    return response.css('a.xst')
    
def parse_article(response: HtmlResponse):
    if response.css('#messagelogin'):
        raise DropItem("login required: %s" % response.url)
    yield {
        'site': 'colg',
        'type': 'article',
        'url': response.url,
        'id': parse_articleid(response.request.url),
        'title': parse_article_title(response),
        'content': parse_article_content(response),
        'writeDate': parse_article_writedate(response),
        'writer': parse_article_writer(response)
    }

def parse_articleid(url):
    return int(REGEX_ARTICLEID.findall(url)[0][0])

def parse_article_title(response: HtmlResponse):
    return response.css('#thread_subject::text').extract_first().strip()

def parse_article_content(response: HtmlResponse):    
    return ''.join(response.css('td.t_f')[0].xpath('node()').extract())

def parse_article_writedate(response: HtmlResponse):
    return response.css('.authi em::text').extract_first().strip().replace('发表于 ', '')

def parse_article_writer(response: HtmlResponse):
    return response.css('.authi a::text').extract_first().strip()

def get_comment_links(response: HtmlResponse, spider: ColgSpider):
    url = []
    lastPageUrls = response.css('.tps a:last-child').xpath('@href').extract()
    for lastPageUrl in lastPageUrls:
        url.extend(get_commentlistpage_urls_near_endof_lastpage(lastPageUrl, spider))
    return url

def get_commentlistpage_urls_near_endof_lastpage(lastPageUrl: str, spider: ColgSpider):
    lastPageNo = get_comment_page_no(lastPageUrl)
    for i in range(0, spider.custom_settings['CRAWLE_RANGE_COMMENT_PAGE']):
        if(lastPageNo - i > 0):
            yield replace_comment_page_no(lastPageUrl, lastPageNo - i)
            
def replace_comment_page_no(url: str, pageNo: int):
    return REGEX_COMMENTPAGE_LINK.sub('thread-\\1-' + str(pageNo) + '-\\3.html', url)

def get_comment_page_no(url):
    if(REGEX_ARTICLEID.match(url)):
        return int(REGEX_ARTICLEID.findall(url)[0][1])
    if(REGEX_COMMENTPAGE_LINK.match(url)):
        return int(REGEX_COMMENTPAGE_LINK.findall(url)[0][1])
    
def get_host_part(url):
    parsed_uri = urlparse(url)
    host_part = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return host_part

def parse_comment(response: HtmlResponse):
    if response.css('#messagelogin'):
        raise DropItem("login required: %s" % response.url)

    commentDivs = response.css('#postlist > div:not(:first-child):not(:last-child)')

    isFirstPage = get_comment_page_no(response.request.url) == 1
    if isFirstPage:
        del commentDivs[0]

    for div in commentDivs:
        yield {
            'site': 'colg',
            'type': 'comment',
            'url': get_host_part(response.url) + parse_comment_url(div),
            'id': parse_comment_id(div),
            'content': parse_comment_content(div),
            'writeDate': parse_comment_writedate(div),
            'writer': parse_comment_writer(div),
            'articleId': parse_articleid(response.request.url)
        }

def parse_comment_url(selector: Selector):
    return selector.css('.pti .authi a::attr(href)').extract_first()

def parse_comment_id(selector: Selector):
    return REGEX_COMMENT_ID.findall(selector.xpath('@id').extract_first())[0]

def parse_comment_content(selector: Selector):
    xpath = './/td[@class="t_f"]/node()'
    return ''.join(selector.xpath(xpath).extract())

def parse_comment_writedate(selector: Selector):
    return selector.css('.authi em::text').extract_first().replace('发表于 ', '').strip()

def parse_comment_writer(selector: Selector):
    return selector.css('.authi a::text').extract_first().strip()
