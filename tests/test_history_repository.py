import datetime as dt

from voc_crawler.history_repository import HistoryRepository

class TestHistoryRepository():

    def test_write(self):
        item = {
            'boardId': 'colg',
            'type': 'article',
            'id': 1
        }
        HistoryRepository.erase(item)
        HistoryRepository.write(item)
        assert HistoryRepository.exist(item) == True
        HistoryRepository.erase(item)
        assert HistoryRepository.exist(item) == False
    
    # def test_getCurrentMonthKey(self):
    #     repo = HistoryRepository()
    #     assert repo.getCurrentMonthKey(dt.date(2018,1,22)) == 1
    #     assert repo.getCurrentMonthKey(dt.date(2018,2,22)) == 1
    #     assert repo.getCurrentMonthKey(dt.date(2018,3,22)) == 1
    #     assert repo.getCurrentMonthKey(dt.date(2018,4,22)) == 4
    #     assert repo.getCurrentMonthKey(dt.date(2018,5,22)) == 4
    #     assert repo.getCurrentMonthKey(dt.date(2018,6,22)) == 4
    #     assert repo.getCurrentMonthKey(dt.date(2018,7,22)) == 7
    #     assert repo.getCurrentMonthKey(dt.date(2018,8,22)) == 7
    #     assert repo.getCurrentMonthKey(dt.date(2018,9,22)) == 7
    #     assert repo.getCurrentMonthKey(dt.date(2018,10,22)) == 10
    #     assert repo.getCurrentMonthKey(dt.date(2018,11,22)) == 10
    #     assert repo.getCurrentMonthKey(dt.date(2018,12,22)) == 10
    
    # def test_getCurrentWeekKey(self):
    #     repo = HistoryRepository()
    #     assert repo.getCurrentWeekKey(dt.date(2018,10,22)) == 43
    #     assert repo.getCurrentWeekKey(dt.date(2018,10,29)) == 43
    #     assert repo.getCurrentWeekKey(dt.date(2018,11,5)) == 45
    #     assert repo.getCurrentWeekKey(dt.date(2018,11,12)) == 45
    #     assert repo.getCurrentWeekKey(dt.date(2018,11,19)) == 47
    #     assert repo.getCurrentWeekKey(dt.date(2018,11,26)) == 47
        
