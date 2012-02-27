"""
Download timeout middleware

See documentation in docs/topics/downloader-middleware.rst
"""
from scrapy.utils.python import WeakKeyCache

from scrapy.middleware import BaseMiddleware

class DownloadTimeoutMiddleware(BaseMiddleware):

    def __init__(self, settings):
        super(DownloadTimeoutMiddleware, self).__init__(settings)
        self._cache = WeakKeyCache(self._download_timeout)

    def _download_timeout(self, spider):
        if hasattr(spider, 'download_timeout'):
            return spider.download_timeout
        return spider.settings.getint('DOWNLOAD_TIMEOUT')

    def process_request(self, request, spider):
        timeout = self._cache[spider]
        if timeout:
            request.meta.setdefault('download_timeout', timeout)
