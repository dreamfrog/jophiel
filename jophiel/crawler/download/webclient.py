from time import time
from urlparse import urlparse, urlunparse, urldefrag

from jophiel.crawler.http import Headers
from jophiel.crawler.utils.httpobj import urlparse_cached
from jophiel.crawler.responsetypes import responsetypes

import httplib2
from . import socks


def _parsed_url_args(parsed):
    path = urlunparse(('', '', parsed.path or '/', parsed.params, parsed.query, ''))
    host = parsed.hostname
    port = parsed.port
    scheme = parsed.scheme
    netloc = parsed.netloc
    if port is None:
        port = 443 if scheme == 'https' else 80
    return scheme, netloc, host, port, path


def _parse(url):
    url = url.strip()
    parsed = urlparse(url)
    return _parsed_url_args(parsed)

httplib2.debuglevel=4

#now only consider http web
class HTTPClient(object):

    def __init__(self, request, timeout=180):
        self.request = request
        
        self.url = urldefrag(request.url)[0]
        self.method = request.method
        self.body = request.body or None
        self.response_headers = None
        self.response_body = None
        self.timeout = request.meta.get('download_timeout') or timeout
        self.start_time = time()
        
        self.headers = {}
        #need make some modify for multi headers,but it is necessary
        for key, values in request.headers.iteritems():
            for value in values:
                if value:
                    self.headers[key] = value
        # set Host header based on url
        # self.headers.setdefault('Host', self.netloc)

        self._set_connection_attributes(request)
        self._set_proxy(request)
        self._build_http()
        
    def _build_http(self):
        #at this time ,don`t consider Authentication
        self.http = httplib2.Http(proxy_info = self.proxy_info,
                                  timeout = self.timeout,
                                  )
        self.http.ignore_etag = True
        self.http.follow_redirects = False
        self.follow_all_redirects = False
        #make sure that all connection has common response,and let high level process error
        self.force_exception_to_status_code = True
        
    def fetch(self):
        print self.headers
        self.response_headers, self.response_body = self.http.request(self.url, self.method, 
                                          body=self.body,headers = self.headers)
        self.headers_time = time()
        return self._build_response(self.response_headers,self.response_body, self.request)
        
    def _set_proxy(self,request):
        self.proxy_info = None
        proxy = request.meta.get('proxy')
        if proxy:
            scheme, _, host, port, _ = _parse(proxy)
            """TODO need seperate https or http proxy"""
            if scheme =="http":
                self.proxy_info = httplib2.ProxyInfo(socks.PROXY_TYPE_HTTP, host, port)      

    def _set_connection_attributes(self, request):
        parsed = urlparse_cached(request)
        self.scheme, self.netloc, self.host, self.port, self.path = _parsed_url_args(parsed)
    
    def _set_body(self,request):
        # set Content-Length based len of body
        if self.body is not None:
            self.headers['Content-Length'] = len(self.body)
            # just in case a broken http/1.1 decides to keep connection alive
            self.headers.setdefault("Connection", "close")        

    def _build_response(self, response_heades,body, request):
        request.meta['download_latency'] = self.headers_time-self.start_time
        status = int(self.response_headers.status)
        headers = Headers(self.response_headers)
        respcls = responsetypes.from_args(headers=headers, url=self.url,body=body)
        return respcls(url=self.url, status=status, headers=headers, body=body)


