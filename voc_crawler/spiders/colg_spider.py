import re
from urllib.parse import urlparse

from scrapy import Spider
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import Join
from scrapy.exceptions import DropItem
from scrapy.http.response.html import HtmlResponse
from scrapy.selector import Selector

class ColgSpider(Spider):
    HOST = 'http://bbs.colg.cn'
    # MAX_PAGE = 10
    MAX_PAGE = 1
    name = 'colg'
    urls = ['http://bbs.colg.cn/forum-171-{0}.html'.format(n) for n in range(1,MAX_PAGE+1)]
    start_urls = urls

    def parse(self, response: HtmlResponse):
        # yield response.follow('http://bbs.colg.cn/thread-7113696-1-1.html', parse_comment)
        # yield response.follow('http://bbs.colg.cn/thread-7113696-1-1.html', parse_article)
        
        articleLinks = get_article_links(response)
        # for articleLink in articleLinks:
        #     yield response.follow(articleLink, parse_article)

        for articleLink in articleLinks:
            yield response.follow(articleLink, parse_comment) #comments in first page

        commentLinks = get_comment_links(response)
        for commentLink in commentLinks:
            yield response.follow(commentLink, parse_comment)

REGEX_ARTICLEID = re.compile(r'http://bbs.colg.cn/thread-(\d*)-(\d*)-1.html')
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


def get_comment_links(response: HtmlResponse):
    return response.css('.tps a')

def get_comment_page_no(url):
    return int(REGEX_ARTICLEID.findall(url)[0][1])
    
def get_host_part(url):
    parsed_uri = urlparse(url)
    host_part = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return host_part

def parse_comment(response: HtmlResponse):
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
