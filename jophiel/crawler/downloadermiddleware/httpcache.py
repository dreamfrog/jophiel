from __future__ import with_statement

import os
from os.path import join, exists
from time import time

from jophiel.crawler.utils.url import canonicalize_url
from jophiel.crawler.w3lib.http import headers_dict_to_raw,headers_raw_to_dict
from jophiel.crawler.http import Headers
from jophiel.crawler.responsetypes import responsetypes
from jophiel.storage.columns import ColumnsField
from jophiel.storage.columns import BaseModel

from jophiel.crawler.conf import CACHE_TABLE_NAME
from jophiel.crawler.storage import WebPage

class HttpCacheMiddleware(object):
    ignore_http_codes = []
    _db = None

    @classmethod
    def db(cls):
        if not cls._db:
            cls._db =  WebPage(CACHE_TABLE_NAME)
        return cls._db
    
    @classmethod
    def process_request(cls, request, spider):
        if not cls.is_cacheable(request):
            return
        response = cls.db().retrieve_response(spider, request)
        if response and cls.is_cacheable_response(response):
            response.flags.append('cached')
            return response
        return None
    
    @classmethod
    def process_response(cls, request, response, spider):
        if cls.is_cacheable(request) and cls.is_cacheable_response(response):
            cls.db().store_response(spider, request, response)
        return response
    
    @classmethod
    def is_cacheable_response(self, response):
        return True

    @classmethod
    def is_cacheable(self, request):
        return True

