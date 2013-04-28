# coding: u8

import json
from itertools import izip

from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from scrapy.utils.response import get_base_url
from scrapy.utils.url import urljoin_rfc

from bdmms.items import BdmmsItem


import logging
from scrapy.log import ScrapyFileLogObserver

logfile = open('bdmms.log', 'a')
log_observer = ScrapyFileLogObserver(logfile, level=logging.DEBUG)
log_observer.start()


class BdmmSpider(BaseSpider):
    # scrapy内建属性
    name = 'bdmms'
    allowed_domains = ['music.baidu.com']
    start_urls = ['http://music.baidu.com/artist']

    # 自定义属性
    host = 'http://music.baidu.com'

    def parse(self, response):
        '''从入口地址[歌手列表开始抓取]'''

        a = '/html/body/div[3]/div/div/div[3]/ul/li[position()>1]/ul/li/a/'
        singer_names = self._query(a + 'text()', response)
        singer_links = self._query(a + '@href', response)

        # 进入单页抓取
        for name, link in izip(singer_names, singer_links):
            yield Request(
                url=self.host + link,
                meta={'item': BdmmsItem(singer=name)},
                callback=self.parse_single_singer)

    def parse_single_singer(self, response):
        '''歌手单页抓取歌手信息以及歌曲列表'''
        # 歌手的id
        artist_id = response.url.strip('/').rsplit('/', 1)[1]

        item = response.meta['item']
        item['singer_face'] = self._get0(self._query(
            '//*[@id="baseInfo"]//span[@class="cover"]/img/@src', response))

        # 分页的ajax地址
        plink = self.host + '/data/user/getsongs?start={0}&ting_uid={1}'
        plink += '&order=hot&.r={2}'
        start = 0
        step = 20
        page_nums = self._query(
            '//div[@id="songList"]//*[contains(@class, "navigator")]/text()',
            response,
            False).re('\d+')
        stop = (int(page_nums[-1]) - 1) * 20 if page_nums else 20
        stop += 1
        # 遍历所有的页码[ajax返回json数据]
        while start < stop:
            yield Request(
                url=plink.format(start, artist_id, self._r()),
                meta={'item': item},
                callback=self.parse_song_page)
            start += step

    def parse_single_song(self, response):
        '''对每一首歌曲解析'''
        item = response.meta['item']
        base_info = '//ul[contains(@class, "base-info")]/li/'

        a = base_info + 'a[contains(@href, "/album/")]/'
        album = self._query(a + 'text()', response)
        album_name = self._get0(album)
        if album_name is not None:
            album_name = album_name.strip(u'《》').strip()
        item['album_name'] = album_name
        item['album_link'] = self._get0(self._query(a + '@href', response))

        item['release_date'] = self._get0(self._query(
            base_info + 'text()', response, False).re('\d{4}-\d{2}-\d{2}'))
        item['tags'] = self._query(
            base_info + '/a[@class="tag-list"]/text()', response)

        lrc_link = self._get0(self._query(
            '//a[@data-lyricdata]/@data-lyricdata', response))
        if lrc_link:
            lrc_link = self.host + json.loads(lrc_link)['href']
            return Request(
                url=lrc_link,
                meta={'item': item},
                callback=self.parse_lrc)
        elif item['album_link']:
            return self._request_get_album(item)
        else:
            return item

    def _request_get_album(self, item):
        return Request(
            url= self.host + item['album_link'],
            meta={'item': item},
            callback=self.parse_album)

    def parse_lrc(self, response):
        '''获取歌词'''
        item = response.meta['item']
        item['lrc'] = response.body
        if item['album_link']:
            return self._request_get_album(item)
        else:
            return item

    def parse_album(self, response):
        '''获取专辑信息'''
        item = response.meta['item']
        item['album_cover'] = self._get0(self._query(
            '//div[@class="album-info"]//span[@class="cover"]/img/@src',
            response))
        item['album_intro'] = self._get0(self._query(
            '//span[@class="description-all"]/text()', response))
        return item

    @staticmethod
    def _get0(x):
        return x[0].strip() if x else None

    def parse_song_page(self, response):
        '''解析歌曲列表分页ajax请求返回的数据'''
        item = response.meta['item']
        html = response.body
        if 'title' not in html:
            yield item
        else:
            html = json.loads(html)['data']['html']
            response = response.replace(body=html)
            a = '//span[contains(@class, "song-title")]/a/'
            song_names = self._query(a + '@title', response)
            song_links = self._query(a + '@href', response)
            for name, link in izip(song_names, song_links):
                # 复制一个，因为每首歌曲的以下属性不同，不然后者会覆盖前者
                item = item.copy()
                item['song_name'] = name.strip()
                item['song_link'] = link
                yield Request(
                    url=self.host + link,
                    meta={'item': item},
                    callback=self.parse_single_song)

    @staticmethod
    def _query(xpath, response, extract=True):
        ret = HtmlXPathSelector(response).select(xpath)
        return ret.extract() if extract else ret

    @staticmethod
    def _r():
        import random
        return str(random.random())
