from scrapy.exceptions import NotConfigured
from scrapy.utils.request import request_httprepr
from scrapy.utils.response import response_httprepr
from scrapy.stats import stats


from scrapy.middleware import BaseMiddleware
from scrapy.meta import BooleanField

class DownloaderStats(BaseMiddleware):
    downloader_stats_enable = BooleanField(default=True)

    def __init__(self, settings):
        super(DownloaderStats, self).__init__(settings)
        if not self.downloader_stats_enable.to_value():
            raise NotConfigured

    def process_request(self, request, spider):
        stats.inc_value('downloader/request_count', spider=spider)
        stats.inc_value('downloader/request_method_count/%s' % request.method, spider=spider)
        reqlen = len(request_httprepr(request))
        stats.inc_value('downloader/request_bytes', reqlen, spider=spider)

    def process_response(self, request, response, spider):
        stats.inc_value('downloader/response_count', spider=spider)
        stats.inc_value('downloader/response_status_count/%s' % response.status, spider=spider)
        reslen = len(response_httprepr(response))
        stats.inc_value('downloader/response_bytes', reslen, spider=spider)
        return response

    def process_exception(self, request, exception, spider):
        ex_class = "%s.%s" % (exception.__class__.__module__, exception.__class__.__name__)
        stats.inc_value('downloader/exception_count', spider=spider)
        stats.inc_value('downloader/exception_type_count/%s' % ex_class, spider=spider)
