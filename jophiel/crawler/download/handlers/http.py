"""Download handlers for http and https schemes"""

from ..webclient import HTTPClient

class HttpDownloadHandler(object):
    def __init__(self, httpclientfactory=HTTPClient):
        self.httpclientfactory = httpclientfactory
    
    def download_request(self, request):
        """Return a deferred for the HTTP download"""
        factory = self.httpclientfactory(request)
        return factory.fetch()
        
        