"""
Download timeout middleware
"""

from jophiel.crawler.conf import DOWNLOAD_TIMEOUT

def download_timeout(spider):
    if hasattr(spider, 'download_timeout'):
        return spider.download_timeout
    return int(DOWNLOAD_TIMEOUT)
 
class DownloadTimeoutMiddleware(object):

    @classmethod
    def process_request(self, request, spider):
        timeout = download_timeout(spider)
        if timeout:
            request.meta.setdefault('download_timeout', timeout)
