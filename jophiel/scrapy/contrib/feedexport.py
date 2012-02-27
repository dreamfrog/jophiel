"""
Feed Exports extension

See documentation in docs/topics/feed-exports.rst
"""

import sys, os, posixpath
from tempfile import TemporaryFile
from datetime import datetime
from urlparse import urlparse
from ftplib import FTP

from zope.interface import Interface, implements
from twisted.internet import defer, threads
from w3lib.url import file_uri_to_path

from scrapy import log, signals
from scrapy.xlib.pydispatch import dispatcher
from scrapy.utils.ftp import ftp_makedirs_cwd
from scrapy.exceptions import NotConfigured
from scrapy.utils.misc import load_object

from scrapy.middleware import BaseMiddleware
from scrapy.meta import StringField
from scrapy.meta import HashField
from scrapy.meta import BooleanField


class IFeedStorage(Interface):
    """Interface that all Feed Storages must implement"""

    def __init__(uri):
        """Initialize the storage with the parameters given in the URI"""

    def open(spider):
        """Open the storage for the given spider. It must return a file-like
        object that will be used for the exporters"""

    def store(file):
        """Store the given file stream"""


class BlockingFeedStorage(object):

    implements(IFeedStorage)

    def open(self, spider):
        return TemporaryFile(prefix='feed-')

    def store(self, file):
        return threads.deferToThread(self._store_in_thread, file)

    def _store_in_thread(self, file):
        raise NotImplementedError


class StdoutFeedStorage(object):

    implements(IFeedStorage)

    def __init__(self, uri, _stdout=sys.stdout):
        self._stdout = _stdout

    def open(self, spider):
        return self._stdout

    def store(self, file):
        pass

class FileFeedStorage(object):

    implements(IFeedStorage)

    def __init__(self, uri):
        self.path = file_uri_to_path(uri)

    def open(self, spider):
        dirname = os.path.dirname(self.path)
        if dirname and not os.path.exists(dirname):
            os.makedirs(dirname)
        return open(self.path, 'ab')

    def store(self, file):
        file.close()

class FTPFeedStorage(BlockingFeedStorage):

    def __init__(self, uri):
        u = urlparse(uri)
        self.host = u.hostname
        self.port = int(u.port or '21')
        self.username = u.username
        self.password = u.password
        self.path = u.path

    def _store_in_thread(self, file):
        file.seek(0)
        ftp = FTP()
        ftp.connect(self.host, self.port)
        ftp.login(self.username, self.password)
        dirname, filename = posixpath.split(self.path)
        ftp_makedirs_cwd(ftp, dirname)
        ftp.storbinary('STOR %s' % filename, file)
        ftp.quit()


class SpiderSlot(object):
    def __init__(self, file, exporter, storage, uri):
        self.file = file
        self.exporter = exporter
        self.storage = storage
        self.uri = uri
        self.itemcount = 0


FEED_URI = None
FEED_URI_PARAMS = None # a function to extend uri arguments
FEED_FORMAT = 'jsonlines'
FEED_STORE_EMPTY = False
FEED_STORAGES = {}
FEED_STORAGES_BASE = {
    '': 'scrapy.contrib.feedexport.FileFeedStorage',
    'file': 'scrapy.contrib.feedexport.FileFeedStorage',
    'stdout': 'scrapy.contrib.feedexport.StdoutFeedStorage',
    's3': 'scrapy.contrib.feedexport.S3FeedStorage',
    'ftp': 'scrapy.contrib.feedexport.FTPFeedStorage',
}
FEED_EXPORTERS = {}
FEED_EXPORTERS_BASE = {
    'json': 'scrapy.contrib.exporter.JsonItemExporter',
    'jsonlines': 'scrapy.contrib.exporter.JsonLinesItemExporter',
    'csv': 'scrapy.contrib.exporter.CsvItemExporter',
    'xml': 'scrapy.contrib.exporter.XmlItemExporter',
    'marshal': 'scrapy.contrib.exporter.MarshalItemExporter',
    'pickle': 'scrapy.contrib.exporter.PickleItemExporter',
}

class FeedExporter(BaseMiddleware):
    
    feed_url = StringField(default=None)
    feed_url_params = StringField(default=None)
    feed_format = StringField(default="jsonlines")
    feed_store_empty = BooleanField(default=False)
    feed_storage = HashField(default={
        '': 'scrapy.contrib.feedexport.FileFeedStorage',
        'file': 'scrapy.contrib.feedexport.FileFeedStorage',
        'stdout': 'scrapy.contrib.feedexport.StdoutFeedStorage',
        's3': 'scrapy.contrib.feedexport.S3FeedStorage',
        'ftp': 'scrapy.contrib.feedexport.FTPFeedStorage',
        })
    feed_exporters = HashField(default={             
        'json': 'scrapy.contrib.exporter.JsonItemExporter',
        'jsonlines': 'scrapy.contrib.exporter.JsonLinesItemExporter',
        'csv': 'scrapy.contrib.exporter.CsvItemExporter',
        'xml': 'scrapy.contrib.exporter.XmlItemExporter',
        'marshal': 'scrapy.contrib.exporter.MarshalItemExporter',
        'pickle': 'scrapy.contrib.exporter.PickleItemExporter',
        })
    
    def __init__(self, settings):
        super(FeedExporter, self).__init__(settings)
        
        self.urifmt = self.feed_url.to_value()
        if not self.urifmt:
            raise NotConfigured
        self.format = self.feed_format.to_value().lower()
        self.storages = self._load_components(self.feed_storage)
        self.exporters = self._load_components(self.feed_exporters)
        if not self._storage_supported(self.urifmt):
            raise NotConfigured
        if not self._exporter_supported(self.format):
            raise NotConfigured
        self.store_empty = settings.getbool('FEED_STORE_EMPTY')
        uripar = settings['FEED_URI_PARAMS']
        self._uripar = load_object(uripar) if uripar else lambda x, y: None
        self.slots = {}
        dispatcher.connect(self.open_spider, signals.spider_opened)
        dispatcher.connect(self.close_spider, signals.spider_closed)
        dispatcher.connect(self.item_scraped, signals.item_scraped)

    def open_spider(self, spider):
        uri = self.urifmt % self._get_uri_params(spider)
        storage = self._get_storage(uri)
        file = storage.open(spider)
        exporter = self._get_exporter(file)
        exporter.start_exporting()
        self.slots[spider] = SpiderSlot(file, exporter, storage, uri)

    def close_spider(self, spider):
        slot = self.slots.pop(spider)
        if not slot.itemcount and not self.store_empty:
            return
        slot.exporter.finish_exporting()
        logfmt = "%%s %s feed (%d items) in: %s" % (self.format, \
            slot.itemcount, slot.uri)
        d = defer.maybeDeferred(slot.storage.store, slot.file)
        d.addCallback(lambda _: log.msg(logfmt % "Stored", spider=spider))
        d.addErrback(log.err, logfmt % "Error storing", spider=spider)
        return d

    def item_scraped(self, item, spider):
        slot = self.slots[spider]
        slot.exporter.export_item(item)
        slot.itemcount += 1
        return item

    def _load_components(self, items):
        conf = items.to_value()
        d = {}
        for k, v in conf.items():
            try:
                d[k] = load_object(v)
            except NotConfigured:
                pass
        return d

    def _exporter_supported(self, format):
        if format in self.exporters:
            return True
        log.msg("Unknown feed format: %s" % format, log.ERROR)

    def _storage_supported(self, uri):
        scheme = urlparse(uri).scheme
        if scheme in self.storages:
            try:
                self._get_storage(uri)
                return True
            except NotConfigured:
                log.msg("Disabled feed storage scheme: %s" % scheme, log.ERROR)
        else:
            log.msg("Unknown feed storage scheme: %s" % scheme, log.ERROR)

    def _get_exporter(self, *a, **kw):
        return self.exporters[self.format](*a, **kw)

    def _get_storage(self, uri):
        return self.storages[urlparse(uri).scheme](uri)

    def _get_uri_params(self, spider):
        params = {}
        for k in dir(spider):
            params[k] = getattr(spider, k)
        ts = datetime.utcnow().replace(microsecond=0).isoformat().replace(':', '-')
        params['time'] = ts
        self._uripar(params, spider)
        return params
