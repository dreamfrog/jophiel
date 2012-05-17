'''
Created on 2012-5-11

@author: lzz
'''

from .http import Request
from .utils.misc import arg_to_iter
from .utils.trackref import object_ref
from .utils.url import url_is_from_spider
from .utils.spider import iterate_spider_output

import copy
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

    def log(self, message, level=logging.DEBUG):
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


def identity(x):
    return x

class Rule(object):

    def __init__(self, link_extractor, callback=None, cb_kwargs=None, follow=None, process_links=None, process_request=identity):
        self.link_extractor = link_extractor
        self.callback = callback
        self.cb_kwargs = cb_kwargs or {}
        self.process_links = process_links
        self.process_request = process_request
        if follow is None:
            self.follow = False if callback else True
        else:
            self.follow = follow

class CrawlSpider(BaseSpider):

    rules = ()

    def __init__(self, *a, **kw):
        super(CrawlSpider, self).__init__(*a, **kw)
        self._compile_rules()

    def parse(self, response):
        return self._parse_response(response, self.parse_start_url, cb_kwargs={}, follow=True)

    def parse_start_url(self, response):
        return []

    def process_results(self, response, results):
        return results

    def _requests_to_follow(self, response):
        seen = set()
        for n, rule in enumerate(self._rules):
            links = [l for l in rule.link_extractor.extract_links(response) if l not in seen]
            if links and rule.process_links:
                links = rule.process_links(links)
            seen = seen.union(links)
            for link in links:
                r = Request(url=link.url, callback=self._response_downloaded)
                r.meta.update(rule=n, link_text=link.text)
                yield rule.process_request(r)

    def _response_downloaded(self, response):
        rule = self._rules[response.meta['rule']]
        return self._parse_response(response, rule.callback, rule.cb_kwargs, rule.follow)

    def _parse_response(self, response, callback, cb_kwargs, follow=True):
        if callback:
            cb_res = callback(response, **cb_kwargs) or ()
            cb_res = self.process_results(response, cb_res)
            for requests_or_item in iterate_spider_output(cb_res):
                yield requests_or_item

        if follow :
            for request_or_item in self._requests_to_follow(response):
                yield request_or_item
                

    def _compile_rules(self):
        def get_method(method):
            if callable(method):
                return method
            elif isinstance(method, basestring):
                return getattr(self, method, None)

        self._rules = [copy.copy(r) for r in self.rules]
        for rule in self._rules:
            rule.callback = get_method(rule.callback)
            rule.process_links = get_method(rule.process_links)
            rule.process_request = get_method(rule.process_request)

class Spider(BaseSpider):
    
    def __init__(self,name,settings,**kwargs):
        super(Spider,self).__init__(name)
        self.settings = settings