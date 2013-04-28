# coding: u8

from scrapy.item import Item, Field


class BdmmsItem(Item):
    # 歌名
    song_name = Field()
    # 歌曲在百度mp3中的url
    song_link = Field()

    # 歌手
    singer = Field()
    # 歌手封面
    singer_face = Field()

    # 所属专辑
    album_name = Field()
    album_link = Field()
    # 专辑发行时间
    release_date = Field()
    # 所属公司
    company = Field()
    # 专辑封面
    album_cover = Field()
    # 专辑简介
    album_intro = Field()

    # 标签
    tags = Field()

    # 歌词
    lrc = Field()

    def copy(self):
        '''文档上面说可以用copy，可是我的会报错，所以自己实现一个'''
        return BdmmsItem(dict(self))
