"""
Depth Spider Middleware

See documentation in docs/topics/spider-middleware.rst
"""

import warnings

from scrapy import log
from scrapy.http import Request
from scrapy.exceptions import ScrapyDeprecationWarning

from scrapy.middleware import BaseMiddleware
from scrapy.meta import IntegerField
from scrapy.meta import BooleanField

DEPTH_LIMIT = 0
DEPTH_STATS = True
DEPTH_PRIORITY = 0

class DepthMiddleware(BaseMiddleware):

    depth_limit = IntegerField(default=0)
    depth_stats = BooleanField(default=True)
    depth_prority = IntegerField(default=1)
    depth_stats_verbose = BooleanField(default=True)
    
    def __init__(self, settings):
        super(DepthMiddleware, self).__init__(settings)
        self.maxdepth = self.depth_limit.to_value()
        usestats = self.depth_stats.to_value()
        self.verbose_stats = self.depth_stats_verbose.to_value()
        self.prio = self.depth_prority.to_value()
        if usestats:
            from scrapy.stats import stats
        else:
            stats = None
        self.stats = stats
        
    def process_spider_output(self, response, result, spider):
        def _filter(request):
            if isinstance(request, Request):
                depth = response.request.meta['depth'] + 1
                request.meta['depth'] = depth
                if self.prio:
                    request.priority -= depth * self.prio
                if self.maxdepth and depth > self.maxdepth:
                    log.msg("Ignoring link (depth > %d): %s " % (self.maxdepth, request.url), \
                        level=log.DEBUG, spider=spider)
                    return False
                elif self.stats:
                    if self.verbose_stats:
                        self.stats.inc_value('request_depth_count/%s' % depth, spider=spider)
                    self.stats.max_value('request_depth_max', depth, spider=spider)
            return True

        # base case (depth=0)
        if self.stats and 'depth' not in response.request.meta: 
            response.request.meta['depth'] = 0
            if self.verbose_stats:
                self.stats.inc_value('request_depth_count/0', spider=spider)

        return (r for r in result or () if _filter(r))
