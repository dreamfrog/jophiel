from collections import defaultdict

from scrapy import log
from scrapy.exceptions import NotConfigured
from scrapy.utils.misc import load_object
from scrapy.utils.defer import process_parallel, process_chain, process_chain_both

from operator import itemgetter
from scrapy.meta import SettingObject
from scrapy.meta import HashField 

class MiddlewareManager(SettingObject):
    """Base class for implementing middleware managers"""

    component_name = 'foo middleware'
    
    middleware_lists = HashField(default={})
    
    def __init__(self, settings, crawler=None):
        super(MiddlewareManager, self).__init__(settings)
        self.crawler = crawler
        
        self.middlewares = self.build_middleware()
        self.methods = defaultdict(list)

        for mw in self.middlewares: 
            self._add_middleware(mw)    
    
    def build_component_list(self, custom, *args):
        if isinstance(custom, (list, tuple)):
            return custom
        for args in args:
            custom.update(args)
        return [k for k, v in sorted(custom.items(), key=itemgetter(1)) \
            if v is not None]
        
    def get_middleware_lists(self):
        middlewarelists = self.middleware_lists.to_value()
        return self.build_component_list(middlewarelists)
    
    def build_middleware(self):
        mwlist = self.get_middleware_lists()
        middlewares = []
        for clspath in mwlist:
            try:
                mwcls = load_object(clspath)
                if self.crawler and hasattr(mwcls, 'from_crawler'):
                    mw = mwcls.from_crawler(self.crawler)
                else:
                    mw = mwcls(self.metas)
                middlewares.append(mw)
            except NotConfigured, e:
                if e.args:
                    clsname = clspath.split('.')[-1]
                    log.msg("Disabled %s: %s" % (clsname, e.args[0]), log.WARNING)
        enabled = [x.__class__.__name__ for x in middlewares]
        log.msg("Enabled %ss: %s" % (self.component_name, ", ".join(enabled)), \
            level=log.DEBUG)
        return middlewares


    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings, crawler)    

    def _add_middleware(self, mw):
        if hasattr(mw, 'open_spider'):
            self.methods['open_spider'].append(mw.open_spider)
        if hasattr(mw, 'close_spider'):
            self.methods['close_spider'].insert(0, mw.close_spider)

    def _process_parallel(self, methodname, obj, *args):
        return process_parallel(self.methods[methodname], obj, *args)

    def _process_chain(self, methodname, obj, *args):
        return process_chain(self.methods[methodname], obj, *args)

    def _process_chain_both(self, cb_methodname, eb_methodname, obj, *args):
        return process_chain_both(self.methods[cb_methodname], \
            self.methods[eb_methodname], obj, *args)

    def open_spider(self, spider):
        return self._process_parallel('open_spider', spider)

    def close_spider(self, spider):
        return self._process_parallel('close_spider', spider)
    

class BaseMiddleware(SettingObject):
    
    def __init__(self, settings):
        super(BaseMiddleware, self).__init__(settings)
