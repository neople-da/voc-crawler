from voc_crawler.history_repository import HistoryRepository

class TestHistoryRepository():

    def test_write(self):
        item = {
            'site': 'colg',
            'type': 'article',
            'id': 1
        }
        HistoryRepository.erase(item)
        HistoryRepository.write(item)
        assert HistoryRepository.exist(item) == True
        HistoryRepository.erase(item)
        assert HistoryRepository.exist(item) == False
