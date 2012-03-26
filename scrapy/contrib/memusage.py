"""
MemoryUsage extension

See documentation in docs/topics/extensions.rst
"""

import socket
from pprint import pformat

from twisted.internet import task

from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from scrapy import log
from scrapy.exceptions import NotConfigured
from scrapy.mail import MailSender
from scrapy.stats import stats
from scrapy.utils.memory import get_vmvalue_from_procfs, procfs_supported
from scrapy.utils.engine import get_engine_status

from scrapy.middleware import BaseMiddleware
from scrapy.meta import BooleanField
from scrapy.meta import ListField
from scrapy.meta import IntegerField

class MemoryUsage(BaseMiddleware):
    
    memusage_enable = BooleanField(default=False)
    memusage_notify_mail = ListField(default=[])
    memusage_limit_mb = IntegerField(default=0)
    memusage_warning_mb = IntegerField(default=0)
    memusage_report = BooleanField(default=False)
    
    
    def __init__(self, crawler):
        super(MemoryUsage, self).__init__(crawler.metas)
        if not self.memusage_enable.to_value():
            raise NotConfigured
        if not procfs_supported():
            raise NotConfigured

        self.crawler = crawler
        self.warned = False
        self.notify_mails = self.memusage_notify_mail.to_value()
        self.limit = self.memusage_limit_mb.to_value() * 1024 * 1024
        self.warning = self.memusage_warning_mb.to_value() * 1024 * 1024
        self.report = self.memusage_report.to_value()
        self.mail = MailSender(self.metas)
        dispatcher.connect(self.engine_started, signal=signals.engine_started)
        dispatcher.connect(self.engine_stopped, signal=signals.engine_stopped)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def get_virtual_size(self):
        return get_vmvalue_from_procfs('VmSize')

    def engine_started(self):
        stats.set_value('memusage/startup', self.get_virtual_size())
        self.tasks = []
        tsk = task.LoopingCall(self.update)
        self.tasks.append(tsk)
        tsk.start(60.0, now=True)
        if self.limit:
            tsk = task.LoopingCall(self._check_limit)
            self.tasks.append(tsk)
            tsk.start(60.0, now=True)
        if self.warning:
            tsk = task.LoopingCall(self._check_warning)
            self.tasks.append(tsk)
            tsk.start(60.0, now=True)

    def engine_stopped(self):
        for tsk in self.tasks:
            if tsk.running:
                tsk.stop()

    def update(self):
        stats.max_value('memusage/max', self.get_virtual_size())

    def _check_limit(self):
        if self.get_virtual_size() > self.limit:
            stats.set_value('memusage/limit_reached', 1)
            mem = self.limit / 1024 / 1024
            log.msg("Memory usage exceeded %dM. Shutting down Scrapy..." % mem, level=log.ERROR)
            if self.notify_mails:
                subj = "%s terminated: memory usage exceeded %dM at %s" % \
                        (self.crawler.settings['BOT_NAME'], mem, socket.gethostname())
                self._send_report(self.notify_mails, subj)
                stats.set_value('memusage/limit_notified', 1)
            self.crawler.stop()

    def _check_warning(self):
        if self.warned: # warn only once
            return
        if self.get_virtual_size() > self.warning:
            stats.set_value('memusage/warning_reached', 1)
            mem = self.warning / 1024 / 1024
            log.msg("Memory usage reached %dM" % mem, level=log.WARNING)
            if self.notify_mails:
                subj = "%s warning: memory usage reached %dM at %s" % \
                        (self.crawler.settings['BOT_NAME'], mem, socket.gethostname())
                self._send_report(self.notify_mails, subj)
                stats.set_value('memusage/warning_notified', 1)
            self.warned = True

    def _send_report(self, rcpts, subject):
        """send notification mail with some additional useful info"""
        s = "Memory usage at engine startup : %dM\r\n" % (stats.get_value('memusage/startup') / 1024 / 1024)
        s += "Maximum memory usage           : %dM\r\n" % (stats.get_value('memusage/max') / 1024 / 1024)
        s += "Current memory usage           : %dM\r\n" % (self.get_virtual_size() / 1024 / 1024)

        s += "ENGINE STATUS ------------------------------------------------------- \r\n"
        s += "\r\n"
        s += pformat(get_engine_status())
        s += "\r\n"
        self.mail.send(rcpts, subject, s)
