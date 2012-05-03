# -*- coding: utf-8 -*-
from __future__ import absolute_import

from kombu.utils import cached_property
from datetime import timedelta

from jophiel.utils import timeutils
from jophiel.utils.url import parse_url

import redis

class RedisBackend(object):
    """Redis task result store."""

    redis = redis #redis-py client module.
    host = "localhost" #: default Redis server hostname (`localhost`).
    port = 6379 #: default Redis server port (6379)
    db = 0 #: default Redis db number (0)
    password = None #: default Redis password (:const:`None`)
    max_connections = None #: Maximium number of connections in the pool.

    def __init__(self, host=None, port=None, db=None, password=None,
            expires=None, max_connections=None, url=None, **kwargs):
        super(RedisBackend, self).__init__(**kwargs) 
        if host and '://' in host:
            url, host = host, None
        self.url = url
        uhost = uport = upass = udb = None
        if url:
            uhost,uport,_,upass,udb = parse_url(url)
        self.host = uhost or host or self.host
        self.port = int(uport or port or self.port)
        self.db = udb or db or self.db
        self.password = upass or password or self.password
        self.expires = self.prepare_expires(expires, type=int)
        self.max_connections = (max_connections or self.max_connections)

    def prepare_expires(self, value, type=None):
        if isinstance(value, timedelta):
            value = timeutils.timedelta_seconds(value)
        if value is not None and type:
            return type(value)
        return value
    
    def get(self, key):
        return self.client.get(key)

    def mget(self, keys):
        return self.client.mget(keys)

    def set(self, key, value,_expire=None):
        client = self.client
        expire = _expire if _expire else self.expires
        if expire is not None:
            client.setex(key, value, expire)
        else:
            client.set(key, value)
        #client.publish(key, value)

    def delete(self, key):
        self.client.delete(key)

    @cached_property
    def client(self):
        pool = self.redis.ConnectionPool(host=self.host, port=self.port,
                                         db=self.db, password=self.password,
                                         max_connections=self.max_connections)
        return self.redis.Redis(connection_pool=pool)


if __name__=="__main__":
    b = RedisBackend(url="redis://localhost:6379/0")
    print b.host,b.port,b.db,b.password
    b.set("zhong","wang")
    print b.get("zhong")
    b.delete("zhong")
    print b.get("zhong")