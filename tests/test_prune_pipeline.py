from voc_crawler.pipelines import PrunePipeline
from bs4 import BeautifulSoup, Tag

class TestPrunePipeline():

    def test_remove_meaningless_tags_hiddenBlock_Shouldbe_removed(self):
        pipeline = PrunePipeline()
        soup = BeautifulSoup('<br>test1<div style="position: absolute; display: none">test2</div><div style="position:absolute;display:none">test3</div>', 'html.parser')
        pipeline.remove_meaningless_tags(soup)
        expected = '<br/>test1'
        assert str(soup) == expected

    def test_remove_meaningless_tags_statusBlock_Shouldbe_removed(self):
        pipeline = PrunePipeline()
        soup = BeautifulSoup('<br>test<i class="pstatus"> 本帖最后由 萌の 于 2018-6-11 16:26 编辑 </i><strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>', 'html.parser')
        pipeline.remove_meaningless_tags(soup)
        expected = '<br/>test<strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>'
        assert str(soup) == expected
    
    def test_remove_meaningless_tags_styleTag_Shouldbe_removed(self):
        pipeline = PrunePipeline()
        soup = BeautifulSoup('<br>test<style>.guestviewthumb {margin:10px auto; text-align:center;}.guestviewthumb a {font-size:12px;}.guestviewthumb_cur {cursor:url(http://static.colg.cn/image/common/scf.cur), default; max-width:200px;}.ie6 .guestviewthumb_cur { width:200px !important;}</style><strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>', 'html.parser')
        pipeline.remove_meaningless_tags(soup)
        expected = '<br/>test<strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>'
        assert str(soup) == expected
    
    def test_remove_meaningless_tags_logInLinkBlock_Shouldbe_removed(self):
        pipeline = PrunePipeline()
        soup = BeautifulSoup('<div class="guestviewthumb"><br /><br><a href="member.php?mod=logging&action=login" onclick="showWindow(\'login\', this.href+\'&referer=\'+encodeURIComponent(location));">登录/注册后可看大图</a></div><strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>', 'html.parser')
        pipeline.remove_meaningless_tags(soup)
        expected = '<div class="guestviewthumb"><br/><br/></div><strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>'
        assert str(soup) == expected

    def test_remove_meaningless_tags_mobileAppSignitureBlock_Shouldbe_removed(self):
        #<a href="misc.php?mod=mobile" target="_blank" style="font-size:12px;color:#708090;">来自Colg的全新APP的回复！</a>
        pipeline = PrunePipeline()
        soup = BeautifulSoup('<div class="guestviewthumb"><br /><br><a href="misc.php?mod=mobile" target="_blank" style="font-size:12px;color:#708090;">来自Colg的全新APP的回复！</a></div><strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>', 'html.parser')
        pipeline.remove_meaningless_tags(soup)
        expected = '<div class="guestviewthumb"><br/><br/></div><strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>'
        assert str(soup) == expected
    
    def test_remove_meaningless_tags_qouteBlock_Shouldbe_removed(self):
        # <div class="quote">
        #   <blockquote>
        #     <font size="2">
        #       <a href="http://bbs.colg.cn/forum.php?mod=redirect&amp;goto=findpost&amp;pid=96688575&amp;ptid=7113696" target="_blank">
        #         <font color="#999999">Venimeux 发表于 2018-1-10 20:27</font>
        #       </a>
        #     </font><br>
        #     啊啊啊黑暗武士什么时候有啊！！
        #   </blockquote>
        # </div>
        pipeline = PrunePipeline()
        soup = BeautifulSoup('<div class="guestviewthumb"><br /><br><div class="quote"><blockquote><font size="2"><a href="http://bbs.colg.cn/forum.php?mod=redirect&amp;goto=findpost&amp;pid=96688575&amp;ptid=7113696" target="_blank"><font color="#999999">Venimeux 发表于 2018-1-10 20:27</font></a></font><br>啊啊啊黑暗武士什么时候有啊！！</blockquote></div></div><strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>', 'html.parser')
        pipeline.remove_meaningless_tags(soup)
        expected = '<div class="guestviewthumb"><br/><br/></div><strong><font size="3"><font color="#ff0000">【客户端EX内容】</font></font></strong>'
        assert str(soup) == expected

    def test_swap_img_src_attribute(self):
        pipeline = PrunePipeline()
        soup = BeautifulSoup('<br>test<img file="test.jpg" src="src.jpg"/>', 'html.parser')
        pipeline.swap_img_src_attribute(soup)
        expected = '<br/>test<img src="test.jpg"/>'
        assert str(soup) == expected

    def test_remove_duplicated_br(self):
        pipeline = PrunePipeline()
        soup = BeautifulSoup('<br>test<br><br>test2', 'html.parser')
        pipeline.remove_duplicated_br(soup)
        expected = '<br/>test<br/>test2'
        assert str(soup) == expected

