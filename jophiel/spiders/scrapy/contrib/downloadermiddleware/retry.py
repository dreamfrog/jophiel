"""
An extension to retry failed requests that are potentially caused by temporary
problems such as a connection timeout or HTTP 500 error.

You can change the behaviour of this middleware by modifing the scraping settings:
RETRY_TIMES - how many times to retry a failed page
RETRY_HTTP_CODES - which HTTP response codes to retry

Failed pages are collected on the scraping process and rescheduled at the end,
once the spider has finished crawling all regular (non failed) pages. Once
there is no more failed pages to retry this middleware sends a signal
(retry_complete), so other extensions could connect to that signal.

About HTTP errors to consider:

- You may want to remove 400 from RETRY_HTTP_CODES, if you stick to the HTTP
  protocol. It's included by default because it's a common code used to
  indicate server overload, which would be something we want to retry
"""

from twisted.internet.error import TimeoutError as ServerTimeoutError, DNSLookupError, \
                                   ConnectionRefusedError, ConnectionDone, ConnectError, \
                                   ConnectionLost, TCPTimedOutError
from twisted.internet.defer import TimeoutError as UserTimeoutError

from scrapy import log
from scrapy.exceptions import NotConfigured
from scrapy.utils.response import response_status_message

from scrapy.meta import BooleanField
from scrapy.meta import IntegerField
from scrapy.meta import ListField
from scrapy.middleware import BaseMiddleware

class RetryMiddleware(BaseMiddleware):

    # IOError is raised by the HttpCompression middleware when trying to
    # decompress an empty response
    EXCEPTIONS_TO_RETRY = (ServerTimeoutError, UserTimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError,
                           IOError)

    
    retry_enable = BooleanField(default=True)
    retry_times = IntegerField(default=3)
    retry_http_codes = ListField(default=[500, 503, 504, 400, 408])
    retry_priority_adjust = IntegerField(default= -1)

    def __init__(self, settings):
        super(RetryMiddleware).__init__(settings)
        if not self.retry_enable.to_value():
            raise NotConfigured
        self.max_retry_times = self.retry_times.to_value()
        self.retry_http_codes = set(int(x) for x in self.retry_http_codes.to_value())
        self.priority_adjust = self.retry_priority_adjust.to_value()

    def process_response(self, request, response, spider):
        if 'dont_retry' in request.meta:
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception, self.EXCEPTIONS_TO_RETRY) \
                and 'dont_retry' not in request.meta:
            return self._retry(request, exception, spider)

    def _retry(self, request, reason, spider):
        retries = request.meta.get('retry_times', 0) + 1

        if retries <= self.max_retry_times:
            log.msg("Retrying %s (failed %d times): %s" % (request, retries, reason),
                    spider=spider, level=log.DEBUG)
            retryreq = request.copy()
            retryreq.meta['retry_times'] = retries
            retryreq.dont_filter = True
            retryreq.priority = request.priority + self.priority_adjust
            return retryreq
        else:
            log.msg("Gave up retrying %s (failed %d times): %s" % (request, retries, reason),
                    spider=spider, level=log.DEBUG)
