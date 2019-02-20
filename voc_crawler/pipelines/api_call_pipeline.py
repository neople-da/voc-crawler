import requests

from scrapy.exceptions import DropItem

from voc_crawler.history_repository import HistoryRepository

class ApiCallPipeline(object):
    def __init__(self, apiHost):
        self.apiHost = apiHost

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            apiHost = crawler.settings.get('API_HOST')
        )
        
    def process_item(self, item, spider):
        isArticle = item['type'] == 'article'
        if isArticle:
            try:
                subUrl = spider.custom_settings['VOC_GAME_TYPE'] + '/articles'
                result = requests.post(self.apiHost + subUrl, data= {
                    'ContentsNo': item['id'],
                    'SiteID': spider.custom_settings['VOC_SITE_ID'],
                    'BoardID': spider.custom_settings['VOC_BOARD_ID'],
                    'Title': item['title'],
                    'Content': item['content'],
                    'WriterID': item['writer'],
                    'WriteDate': item['writeDate'],
                    'Link': item['url']
                })
                result.raise_for_status()
                return item
            except Exception as ex:
                HistoryRepository.erase(item)
                if result.status_code == 400:
                    raise DropItem("article not exist: %s" % item)
                else:
                    raise ex
        else:
            try:
                subUrl = f"{spider.custom_settings['VOC_GAME_TYPE']}/comments?siteId={spider.custom_settings['VOC_SITE_ID']}&siteArticleId={item['articleId']}"
                result = requests.post(self.apiHost + subUrl, data= {
                    'SiteCommentID': item['id'],
                    'Content': item['content'],
                    'WriterID': item['writer'],
                    'WriteDate': item['writeDate'],
                    'Link': item['url']
                })
                result.raise_for_status()
                return item
            except Exception as ex:
                HistoryRepository.erase(item)
                if result.status_code == 400:
                    raise DropItem("article not exist: %s" % item)
                else:
                    raise ex
        