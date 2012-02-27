"""
MemoryDebugger extension

See documentation in docs/topics/extensions.rst
"""

import gc

from scrapy.xlib.pydispatch import dispatcher

from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.stats import stats
from scrapy.utils.trackref import live_refs

from scrapy.middleware import BaseMiddleware
from scrapy.meta import BooleanField

class MemoryDebugger(BaseMiddleware):
    
    memdebug_enable = BooleanField(default=False)
    track_refs = BooleanField(default=False)

    def __init__(self, settings):
        super(MemoryDebugger, self).__init__(settings)
        try:
            import libxml2
            self.libxml2 = libxml2
        except ImportError:
            self.libxml2 = None
        if not self.memdebug_enable.to_value():
            raise NotConfigured

        dispatcher.connect(self.engine_started, signals.engine_started)
        dispatcher.connect(self.engine_stopped, signals.engine_stopped)

    def engine_started(self):
        if self.libxml2:
            self.libxml2.debugMemory(1)

    def engine_stopped(self):
        if self.libxml2:
            self.libxml2.cleanupParser()
            stats.set_value('memdebug/libxml2_leaked_bytes', self.libxml2.debugMemory(1))
        gc.collect()
        stats.set_value('memdebug/gc_garbage_count', len(gc.garbage))
        if self.track_refs.to_value():
            for cls, wdict in live_refs.iteritems():
                if not wdict:
                    continue
                stats.set_value('memdebug/live_refs/%s' % cls.__name__, len(wdict))
