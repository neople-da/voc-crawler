from bs4 import BeautifulSoup
from voc_crawler.history_repository import HistoryRepository

class PrunePipeline(object):

    def process_item(self, item, spider):
        try:
            item['content'] = item['content'].replace('\r', '').replace('\n', '').strip()
            soup = BeautifulSoup(item['content'], 'html.parser')        
            self.remove_meaningless_tags(soup)
            self.swap_img_src_attribute(soup)
            self.remove_duplicated_br(soup)
            item['content'] = str(soup)
            return item
        except Exception as ex:
            HistoryRepository.erase(item['id'], item['type'] == 'comment')
            raise ex

    def remove_meaningless_tags(self, soup: BeautifulSoup):
        for element in soup.find_all(self.find_element_to_remove):
            element.decompose()
    
    def swap_img_src_attribute(self, soup: BeautifulSoup):
        for img in soup.find_all('img', file=True):
            img['src'] = img['file']
            del img['file']
    
    def remove_duplicated_br(self, soup: BeautifulSoup):
        for br in soup.find_all('br'):
            if str(br.next_sibling) == '<br/>':
                br.next_sibling.decompose()

    def find_element_to_remove(self, tag):
        if tag.has_attr('style') and ('display:none' in tag['style'] or 'display: none' in tag['style']):
            return True
        if tag.name == 'i' and tag.has_attr('class') and tag['class'] == ['pstatus']:
            return True
        if tag.name == 'a':
            if tag.text == '登录/注册后可看大图' or tag.text == '来自Colg的全新APP的回复！':
                return True
        if tag.name == 'style' or tag.name == 'script':
            return True
        if tag.name == 'div' and tag.has_attr('class'):
            if 'locked' in tag['class'] or 'quote' in tag['class']:
                return True
        else:
            return False