import random
import warnings
from time import time
from collections import deque
from functools import partial

from twisted.internet import reactor, defer
from twisted.python.failure import Failure

from scrapy.utils.defer import mustbe_deferred
from scrapy.utils.signal import send_catch_log
from scrapy.utils.httpobj import urlparse_cached
from scrapy.resolver import dnscache
from scrapy.exceptions import ScrapyDeprecationWarning
from scrapy import signals
from scrapy import log
from .middleware import DownloaderMiddlewareManager
from .handlers import DownloadHandlers

from scrapy import settings

from scrapy.meta import SettingObject
from scrapy.meta import IntegerField
from scrapy.meta import FloatField
from scrapy.meta import BooleanField

class Slot(object):
    """Downloader slot"""

    def __init__(self, concurrency, delay, randomize_delay, settings):
        self.concurrency = concurrency
        self.delay = delay
        self.randomize_delay = randomize_delay
        self.active = set()
        self.queue = deque()
        self.transferring = set()
        self.lastseen = 0

    def free_transfer_slots(self):
        return self.concurrency - len(self.transferring)

    def download_delay(self):
        if self.randomize_delay:
            return random.uniform(0.5 * self.delay, 1.5 * self.delay)
        return self.delay

class Downloader(SettingObject):
    
    concurrent_requests = IntegerField(default=15)
    concurrent_requests_per_domains = IntegerField(default=1)
    concurrent_requests_per_ip = IntegerField(default=1)
    download_delay = FloatField(default=0)
    randomize_delay = BooleanField(default=False)
    
    def __init__(self, metas):
        super(Downloader, self).__init__(metas)
        self.slots = {}
        self.active = set()
        self.handlers = DownloadHandlers()
        self.total_concurrency = self.concurrent_requests.to_value()
        self.domain_concurrency = self.concurrent_requests_per_domains.to_value()
        self.ip_concurrency = self.concurrent_requests_per_ip.to_value()
        
        self.middleware = DownloaderMiddlewareManager(self.metas)

    def _get_concurrency_delay(self, concurrency, spider):
        delay = self.download_delay.to_value()
        if hasattr(spider, 'download_delay'):
            delay = spider.download_delay
    
        if hasattr(spider, 'max_concurrent_requests'):
            concurrency = spider.max_concurrent_requests
    
        if delay > 0:
            concurrency = 1 # force concurrency=1 if download delay required
    
        return concurrency, delay
    
    def fetch(self, request, spider):
        key, slot = self._get_slot(request, spider)

        self.active.add(request)
        slot.active.add(request)
        def _deactivate(response):
            self.active.remove(request)
            slot.active.remove(request)
            if not slot.active: # remove empty slots
                del self.slots[key]
            return response

        dlfunc = partial(self._enqueue_request, slot=slot)
        dfd = self.middleware.download(dlfunc, request, spider)
        return dfd.addBoth(_deactivate)

    def needs_backout(self):
        return len(self.active) >= self.total_concurrency

    def _get_slot(self, request, spider):
        key = urlparse_cached(request).hostname or ''
        if self.ip_concurrency:
            key = dnscache.get(key, key)
        if key not in self.slots:
            if self.ip_concurrency:
                concurrency = self.ip_concurrency
            else:
                concurrency = self.domain_concurrency
            concurrency, delay = self._get_concurrency_delay(concurrency, spider)
            randomize_delay = self.randomize_delay.to_value()
            self.slots[key] = Slot(concurrency, delay, randomize_delay, self.settings)
        return key, self.slots[key]

    def _enqueue_request(self, request, spider, slot):
        def _downloaded(response):
            send_catch_log(signal=signals.response_downloaded, \
                    response=response, request=request, spider=spider)
            return response

        deferred = defer.Deferred().addCallback(_downloaded)
        slot.queue.append((request, deferred))
        self._process_queue(spider, slot)
        return deferred

    def _process_queue(self, spider, slot):
        # Delay queue processing if a download_delay is configured
        now = time()
        delay = slot.download_delay()
        if delay:
            penalty = delay - now + slot.lastseen
            if penalty > 0 and slot.free_transfer_slots():
                d = defer.Deferred()
                d.addCallback(self._process_queue, slot)
                reactor.callLater(penalty, d.callback, spider)
                return
        slot.lastseen = now

        # Process enqueued requests if there are free slots to transfer for this slot
        while slot.queue and slot.free_transfer_slots() > 0:
            request, deferred = slot.queue.popleft()
            dfd = self._download(slot, request, spider)
            dfd.chainDeferred(deferred)

    def _download(self, slot, request, spider):
        # The order is very important for the following deferreds. Do not change!

        # 1. Create the download deferred
        dfd = mustbe_deferred(self.handlers.download_request, request, spider)

        # 2. After response arrives,  remove the request from transferring
        # state to free up the transferring slot so it can be used by the
        # following requests (perhaps those which came from the downloader
        # middleware itself)
        slot.transferring.add(request)
        def finish_transferring(_):
            slot.transferring.remove(request)
            self._process_queue(spider, slot)
            return _
        return dfd.addBoth(finish_transferring)

    def is_idle(self):
        return not self.slots

