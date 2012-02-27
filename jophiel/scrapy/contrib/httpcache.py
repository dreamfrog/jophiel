from __future__ import with_statement

import os
from time import time
import cPickle as pickle

from scrapy.http import Headers
from scrapy.responsetypes import responsetypes
from scrapy.utils.request import request_fingerprint
from scrapy.utils.project import data_path

from scrapy.meta import SettingObject
from scrapy.meta import StringField
from scrapy.meta import IntegerField


class DbmCacheStorage(SettingObject):

    httpcache_dir = StringField(default='httpcache')
    httpcache_expiration_secs = IntegerField(default=0)
    httpcache_dbm_module = StringField(default="anydbm")
    
    def __init__(self, settings):
        self.cachedir = data_path(self.httpcache_dir.to_value())
        self.expiration_secs = self.httpcache_expiration_secs.to_value()
        self.dbmodule = __import__(self.httpcache_dbm_module.to_value())
        self.dbs = {}

    def open_spider(self, spider):
        dbpath = os.path.join(self.cachedir, '%s.db' % spider.name)
        self.dbs[spider] = self.dbmodule.open(dbpath, 'c')

    def close_spider(self, spider):
        self.dbs[spider].close()

    def retrieve_response(self, spider, request):
        data = self._read_data(spider, request)
        if data is None:
            return # not cached
        url = data['url']
        status = data['status']
        headers = Headers(data['headers'])
        body = data['body']
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)
        return response

    def store_response(self, spider, request, response):
        key = self._request_key(request)
        data = {
            'status': response.status,
            'url': response.url,
            'headers': dict(response.headers),
            'body': response.body,
        }
        self.dbs[spider]['%s_data' % key] = pickle.dumps(data, protocol=2)
        self.dbs[spider]['%s_time' % key] = str(time())

    def _read_data(self, spider, request):
        key = self._request_key(request)
        db = self.dbs[spider]
        tkey = '%s_time' % key
        if not db.has_key(tkey):
            return # not found
        ts = db[tkey]
        if 0 < self.expiration_secs < time() - float(ts):
            return # expired
        return pickle.loads(db['%s_data' % key])

    def _request_key(self, request):
        return request_fingerprint(request)
