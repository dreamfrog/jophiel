"""
Base class for Scrapy spiders

See documentation in docs/topics/spiders.rst
"""

from ..http import Request
from ..utils.misc import arg_to_iter
from ..utils.trackref import object_ref
from ..utils.url import url_is_from_spider

import logging

log = logging.getLogger("Spider")

class BaseSpider(object_ref):
    """Base class for scrapy spiders. All spiders must inherit from this
    class.
    """
    name = None

    def __init__(self, name=None, **kwargs):
        if name is not None:
            self.name = name
        elif not getattr(self, 'name', None):
            raise ValueError("%s must have a name" % type(self).__name__)
        self.__dict__.update(kwargs)
        if not hasattr(self, 'start_urls'):
            self.start_urls = []

    def log(self, message, level=log.DEBUG):
        """Log the given messages at the given log level. Always use this
        method to send log messages from your spider
        """
        log.msg(message, spider=self, level=level)

    def start_requests(self):
        reqs = []
        for url in self.start_urls:
            reqs.extend(arg_to_iter(self.make_requests_from_url(url)))
        return reqs

    def make_requests_from_url(self, url):
        return Request(url, dont_filter=True)

    def parse(self, response):
        raise NotImplementedError

    def __str__(self):
        return "<%s %r at 0x%0x>" % (type(self).__name__, self.name, id(self))

    __repr__ = __str__

