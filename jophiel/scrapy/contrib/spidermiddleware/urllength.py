"""
Url Length Spider Middleware

See documentation in docs/topics/spider-middleware.rst
"""

from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import NotConfigured

from scrapy.middleware import BaseMiddleware
from scrapy.meta import IntegerField

class UrlLengthMiddleware(BaseMiddleware):
    
    urllength_limit = IntegerField(default=2083)
    
    def __init__(self, settings):
        super(UrlLengthMiddleware, self).__init__(settings)
        self.maxlength = self.urllength_limit.to_value()

    def process_spider_output(self, response, result, spider):
        def _filter(request):
            if isinstance(request, Request) and len(request.url) > self.maxlength:
                log.msg("Ignoring link (url length > %d): %s " % (self.maxlength, request.url), \
                    level=log.DEBUG, spider=spider)
                return False
            else:
                return True

        return (r for r in result or () if _filter(r))
