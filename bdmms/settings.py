# coding: u8

BOT_NAME = 'bdmms'

SPIDER_MODULES = ['bdmms.spiders']
NEWSPIDER_MODULE = 'bdmms.spiders'

# 抓取时延n秒[scrapy默认会在DOWNLOAD_DELAY的基础上再随机乘上一个0.5~1.5的因子]
# 百度会让输入验证码，为了不让蜘蛛停下来，时延长点
#DOWNLOAD_DELAY = 2

# 禁用cookie
#COOKIES_ENABLED = False

#LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = [
    'bdmms.pipelines.BdmmsPipeline',
    'scrapy_redis.pipelines.RedisPipeline',
]

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'bdmms.rotate_useragent.RotateUserAgentMiddleware': 400,
}

# 数据库设置
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
DB_NAME = 'baidu_music_metadata'
DB_USER = 'root'
DB_PASS = '111'
DB_HOST_M = '127.0.0.1'
DB_PORT = 3306
engine = create_engine(
    'mysql://%s:%s@%s:%s/%s?charset=utf8' %
    (DB_USER, DB_PASS, DB_HOST_M, DB_PORT, DB_NAME),
    encoding='utf8',
    echo=False,
)
db = scoped_session(sessionmaker(bind=engine))


# scrapy_redis
SCHEDULER = "scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
