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
        try:
            subUrl = '/article' if item['type'] == 'article' else f"/comments?siteId=2&siteArticleId={item['articleId']}"
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
            HistoryRepository.erase(item['id'], item['type'] == 'comment')
            if result.status_code == 400:
                raise DropItem("article not exiest: %s" % item)
            else:
                raise ex
        