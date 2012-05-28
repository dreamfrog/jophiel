"""Download handlers for different schemes"""

from jophiel.crawler.utils.misc import load_object
from . import file,http
from jophiel.crawler.utils.httpobj import urlparse_cached
from jophiel.crawler.exceptions import NotSupported

DOWNLOAD_HANDLERS = {
    'file': file.FileDownloadHandler(),
    'http': http.HttpDownloadHandler(),
    'https': http.HttpDownloadHandler(),
}

class DownloadHandlers(object):

    def __init__(self):
        self._handlers = DOWNLOAD_HANDLERS
        self._notconfigured = {}

    def download_request(self, request, spider):
        scheme = urlparse_cached(request).scheme
        try:
            handler = self._handlers[scheme]
        except KeyError:
            msg = self._notconfigured.get(scheme, \
                    'no handler available for that scheme')
            raise NotSupported("Unsupported URL scheme '%s': %s" % (scheme, msg))
        return handler.download_request(request)
