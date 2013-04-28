# coding: u8

from scrapy.http import Request
from scrapy.exceptions import DropItem

from settings import db
from models import Singer, Album, Tag, Song, SongTag


class Empty(object):
    def __getattr__(self, k):
        return None


class BdmmsPipeline(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        if item.get('song_name') is None:
            # 分页完
            raise DropItem('ajax page over.')
        singer = db.query(
            Singer.pk).filter_by(face=item['singer_face']).first()
        if singer is None:
            singer = Singer(name=item['singer'], face=item['singer_face'])
            db.add(singer)

        album_name = item.get('album_name')
        if album_name is not None:
            cover = item.get('album_cover')
            album = db.query(Album.pk).filter_by(cover=cover).first()
            if album is None:
                album = Album(
                    name=album_name,
                    intro=item.get('album_intro'),
                    rdt=item['release_date'],
                    cover=cover)
                db.add(album)
        else:
            album = Empty()

        db.commit()

        lrc = item.get('lrc')
        song = db.query(Song).filter_by(
            name=item['song_name'], singer=singer.pk).first()
        if song is None:
            song = Song(
                name=item['song_name'],
                singer=singer.pk,
                album=album.pk,
                lrc=lrc)
            db.add(song)
            db.commit()
        elif None not in (lrc, song.lrc):
            song.lrc = lrc

        tag_objs = []
        for tag in item['tags']:
            t = db.query(Tag.pk).filter_by(name=tag).first()
            if t is None:
                t = Tag(name=tag)
                db.add(t)
            tag_objs.append(t)
        db.commit()

        for tag in tag_objs:
            db.merge(SongTag(sid=song.pk, tid=tag.pk))
        db.commit()

        return item
