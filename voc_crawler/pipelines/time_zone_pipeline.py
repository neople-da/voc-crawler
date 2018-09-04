from datetime import datetime

class TimeZonePipeline(object):
    
    def process_item(self, item, spider):
        writedate = datetime.strptime(f"{item['writeDate']} {spider.custom_settings['UTC_OFFSET']}", '%Y-%m-%d %H:%M %z')
        item['writeDate'] = writedate.astimezone().strftime('%Y-%m-%d %H:%M')
        return item
    