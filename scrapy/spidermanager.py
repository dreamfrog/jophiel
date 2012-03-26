"""
SpiderManager is the class which locates and manages all website-specific
spiders
"""

from zope.interface import implements

from scrapy import signals
from scrapy.interfaces import ISpiderManager
from scrapy.utils.misc import walk_modules
from scrapy.utils.spider import iter_spider_classes
from scrapy.xlib.pydispatch import dispatcher

from scrapy.meta import SettingObject
from scrapy.meta import ListField

class SpiderManager(SettingObject):

    implements(ISpiderManager)
    
    spider_modules = ListField(default=[])
    
    def __init__(self, settings):
        super(SpiderManager, self).__init__(settings)
        self.modules = self.spider_modules.to_value()
        self._spiders = {}
        for name in self.modules:
            for module in walk_modules(name):
                self._load_spiders(module)
        dispatcher.connect(self.close_spider, signals.spider_closed)

    def _load_spiders(self, module):
        for spcls in iter_spider_classes(module):
            self._spiders[spcls.name] = spcls

    def create(self, spider_name, **spider_kwargs):
        try:
            spcls = self._spiders[spider_name]
        except KeyError:
            raise KeyError("Spider not found: %s" % spider_name)
        return spcls(**spider_kwargs)

    def find_by_request(self, request):
        return [name for name, cls in self._spiders.iteritems()
            if cls.handles_request(request)]

    def list(self):
        return self._spiders.keys()

    def close_spider(self, spider, reason):
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)
