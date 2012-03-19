'''
Created on 2012-2-16

@author: lzz
'''

import signal

from twisted.internet import reactor, defer

from scrapy.xlib.pydispatch import dispatcher
from scrapy.core.engine import ExecutionEngine
from scrapy.resolver import CachingThreadedResolver
from scrapy.extension import ExtensionManager
from scrapy.utils.ossignal import install_shutdown_handlers, signal_names
from scrapy.utils.misc import load_object
from scrapy import log, signals

from scrapy.meta import SettingObject
from scrapy.meta import StringField
from scrapy.meta import BooleanField

class Crawler(SettingObject):
    
    spider_manager_class = StringField(default="scrapy.spidermanager.SpiderManager")
    
    def __init__(self, settings):
        super(Crawler, self).__init__(settings)
        self.configured = False

    def configure(self):
        if self.configured:
            return
        self.configured = True
        self.extensions = ExtensionManager(self.metas, self)
        spman_cls = load_object(self.spider_manager_class.to_value())
        self.spiders = spman_cls(self.metas)
        self.engine = ExecutionEngine(self, self._spider_closed)

    def crawl(self, spider, requests=None):
        spider.set_crawler(self)
        if requests is None:
            requests = spider.start_requests()
        return self.engine.open_spider(spider, requests)

    def _spider_closed(self, spider=None):
        if not self.engine.open_spiders:
            self.stop()

    @defer.inlineCallbacks
    def start(self):
        yield defer.maybeDeferred(self.configure)
        yield defer.maybeDeferred(self.engine.start)

    @defer.inlineCallbacks
    def stop(self):
        if self.engine.running:
            yield defer.maybeDeferred(self.engine.stop)


class CrawlerProcess(Crawler):
    """A class to run a single Scrapy crawler in a process. It provides
    automatic control of the Twisted reactor and installs some convenient
    signals for shutting down the crawl.
    """
    dnscache_enable = BooleanField(default=False)
    
    def __init__(self, settings, *a, **kw):
        super(CrawlerProcess, self).__init__(settings)
        dispatcher.connect(self.stop, signals.engine_stopped)
        install_shutdown_handlers(self._signal_shutdown)

    def start(self):
        super(CrawlerProcess, self).start()
        if self.dnscache_enable.to_value():
            reactor.installResolver(CachingThreadedResolver(reactor))
        reactor.addSystemEventTrigger('before', 'shutdown', self.stop)
        reactor.run(installSignalHandlers=False) # blocking call

    def stop(self):
        d = super(CrawlerProcess, self).stop()
        d.addBoth(self._stop_reactor)
        return d

    def _stop_reactor(self, _=None):
        try:
            reactor.stop()
        except RuntimeError: # raised if already stopped or in shutdown stage
            pass

    def _signal_shutdown(self, signum, _):
        install_shutdown_handlers(self._signal_kill)
        signame = signal_names[signum]
        log.msg("Received %s, shutting down gracefully. Send again to force " \
            "unclean shutdown" % signame, level=log.INFO)
        reactor.callFromThread(self.stop)

    def _signal_kill(self, signum, _):
        install_shutdown_handlers(signal.SIG_IGN)
        signame = signal_names[signum]
        log.msg('Received %s twice, forcing unclean shutdown' % signame, \
            level=log.INFO)
        reactor.callFromThread(self._stop_reactor)

from scrapy.xlib.pydispatch import dispatcher

class CommonCrawler(object):
 
    def __init__(self, settings, spider):
        
        self.settings = settings 
        self.items = []
        self.spider = spider
        
        self.crawler = CrawlerProcess(settings)
        self.crawler.configure()
        
        #configure item passed signals
        dispatcher.connect(self._item_passed, signals.item_passed)
 
    def _item_passed(self, item):
        print "Got item:", item
  
    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        self.crawler.stop()
