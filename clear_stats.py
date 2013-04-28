# coding: u8


import redis


REDIS_HOST = 'localhost'
REDIS_PORT = 6379


def clear_stats():
    open('./bdmms.log', 'w').write('')
    server = redis.Redis(REDIS_HOST, REDIS_PORT)
    for key in ["bdmms:requests", "bdmms:items", "bdmms:dupefilter"]:
        server.delete(key)


if __name__ == "__main__":
    clear_stats()
