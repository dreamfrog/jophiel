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

class WebPage(BaseModel):
    meta = ColumnsField()
    headers = ColumnsField()
    body = ColumnsField()

    def __init__(self,table_name,**kwargs):
        super(WebPage,self).__init__(table_name,**kwargs)
        
    def _get_request_path(self, spider, request):
        return request.request_path
                
    def retrieve_response(self, spider, request):
        """Return response if present in cache, or None otherwise."""
        rpath = self._get_request_path(spider, request)
        result = self.fetch(rpath,*self.columns_name)
        if not result or "meta" not in result:
            return
        
        metadata = result["meta"]
        url = metadata.get('responseUrl')
        status = int(metadata['status'])
        rawheaders = result["headers"]["response"] if "response" in result["headers"] else ""
        body = result["body"]["response"] if "response" in result["body"] else ""
        
        headers = Headers(headers_raw_to_dict(rawheaders))
        respcls = responsetypes.from_args(headers=headers, url=url)
        response = respcls(url=url, headers=headers, status=status, body=body)            
        return response

    def store_response(self, spider, request, response):
        """Store the given response in the cache."""
        rpath = self._get_request_path(spider, request)
        metadata = {}
        for x in ['url','method'] :
            if hasattr(request,x):
                metadata[x] = str(getattr(request,x))
        for x in ['status','encoding']:
            if hasattr(response,x):
                metadata[x] = str(getattr(response,x))
        metadata["responseUrl"] = response.url
        metadata["lastModified"] = time.strftime("%Y-%m-%d %H:%M:%S")
        body = {
               "request":request.body,
               "response":response.body
               }
        headers = {
                "request":headers_dict_to_raw(request.headers),
                "response":headers_dict_to_raw(response.headers),
                }    
        self.save(rpath,meta=metadata,body=body,headers=headers)

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

