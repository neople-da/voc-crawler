import re
from scrapy.http.response.html import HtmlResponse

INVEN_HOST = 'http://www.inven.co.kr/board/'
REGEX_ARTICLEID = re.compile(INVEN_HOST + r'[a-zA-Z]+/\d*/(\d*)')

def get_article_links(response: HtmlResponse):
    return response.css('.ls.tr .bbsSubject a')

def parse_article_base(gameName, boardId, response: HtmlResponse):
    yield {
        'boardId': f'inven:{gameName}:{boardId}',
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
    return response.css('.articleTitle h1::text').extract_first().strip()

def parse_article_content(response: HtmlResponse):    
    return ''.join(response.css('#powerbbsContent')[0].xpath('node()').extract()).strip()

def parse_article_writedate(response: HtmlResponse):
    return response.css('.articleDate::text').extract_first().strip()

def parse_article_writer(response: HtmlResponse):
    return response.css('.articleWriter span::text').extract_first().strip()