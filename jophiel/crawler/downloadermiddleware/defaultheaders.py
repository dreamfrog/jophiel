"""
DefaultHeaders downloader middleware

See documentation in docs/topics/downloader-middleware.rst
"""
from jophiel.crawler.utils.python import WeakKeyCache
from jophiel.crawler import conf  

DEFAULT_REQUEST_HEADERS  = conf.DEFAULT_REQUEST_HEADERS

def default_headers(spider):
    return DEFAULT_REQUEST_HEADERS.items()

class DefaultHeadersMiddleware(object):

    @classmethod
    def process_request(cls, request, spider):
        for k, v in default_headers(spider):
            request.headers.setdefault(k, v)
