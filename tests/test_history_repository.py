from voc_crawler.history_repository import HistoryRepository

class TestHistoryRepository():

    def test_write(self):
        HistoryRepository.erase(1)
        HistoryRepository.write(1)
        assert HistoryRepository.exist(1) == True
        HistoryRepository.erase(1)
        assert HistoryRepository.exist(1) == False
