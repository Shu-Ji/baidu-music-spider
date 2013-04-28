#coding:utf-8

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Text, Date
from sqlalchemy.schema import PrimaryKeyConstraint


Base = declarative_base()


class Singer(Base):
    '''歌手表'''
    __tablename__ = 'singer'

    pk = Column(Integer, primary_key=True, autoincrement=True)
    # 歌手名
    name = Column(String(50), index=True)
    # 封面url
    face = Column(String(200))


class Tag(Base):
    '''标签表'''
    __tablename__ = 'tag'

    pk = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=True, index=True)


class Album(Base):
    '''专辑表'''
    __tablename__ = 'album'

    pk = Column(Integer, primary_key=True, autoincrement=True)
    # 专辑名
    name = Column(String(100), nullable=True, index=True)
    # 简介
    intro = Column(Text)
    # 发行时间[release date]
    rdt = Column(Date)
    # 所属公司
    corp = Column(String(50))
    # 封面url
    cover = Column(String(200))


class Song(Base):
    '''歌曲表'''
    __tablename__ = 'song'

    pk = Column(Integer, primary_key=True, autoincrement=True)
    # 歌名
    name = Column(String(100), nullable=True, index=True)
    # 歌手id
    singer = Column(Integer, nullable=True, index=True)
    # 所属专辑id
    album = Column(Integer)
    # 歌词
    lrc = Column(Text)


class SongTag(Base):
    '''歌曲与标签关系表'''
    __tablename__ = 'song_and_tag'
    __table_args__ = (PrimaryKeyConstraint('sid', 'tid', name='sid_tid_pkc'),)

    # 歌曲id
    sid = Column(Integer, nullable=True, index=True)
    # 标签id
    tid = Column(Integer, nullable=True, index=True)


def init_db():
    # 创建各个表
    import settings
    metadata = Base.metadata
    metadata.create_all(settings.engine)


if __name__ == '__main__':
    init_db()
