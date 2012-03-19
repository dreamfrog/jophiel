from __future__ import with_statement

import os, cPickle as pickle

from scrapy import signals
from scrapy.xlib.pydispatch import dispatcher

from scrapy.middleware import BaseMiddleware
from scrapy.meta import StringField

class SpiderState(BaseMiddleware):
    """Store and load spider state during a scraping job"""
    
    jobdir = StringField(default="")
    
    def __init__(self, settings, jobdir=None):
        super(SpiderState, self).__init__(settings)
        self.jobdir = jobdir

    @classmethod
    def from_crawler(cls, crawler):
        obj = cls(crawler.metas)
        dispatcher.connect(obj.spider_closed, signal=signals.spider_closed)
        dispatcher.connect(obj.spider_opened, signal=signals.spider_opened)
        return obj

    def spider_closed(self, spider):
        if self.jobdir:
            with open(self.statefn, 'wb') as f:
                pickle.dump(spider.state, f, protocol=2)

    def spider_opened(self, spider):
        if self.jobdir and os.path.exists(self.statefn):
            with open(self.statefn) as f:
                spider.state = pickle.load(f)
        else:
            spider.state = {}

    @property
    def statefn(self):
        return os.path.join(self.jobdir, 'spider.state')
