"""
This module implements the Request class which is used to represent HTTP
requests in Scrapy.

See documentation in docs/topics/request-response.rst
"""

import copy
import hashlib

from ..headers import Headers
from jophiel.crawler.utils.trackref import object_ref
from jophiel.crawler.utils.decorator import deprecated
from jophiel.crawler.utils.url import escape_ajax
from jophiel.crawler.utils.url import canonicalize_url
from jophiel.crawler.w3lib.http import headers_dict_to_raw,headers_raw_to_dict
from jophiel.crawler.w3lib.url import safe_url_string


class Request(object_ref):

    def __init__(self, url, callback=None, method='GET', headers=None, body=None, 
                 cookies=None, meta=None, encoding='utf-8', priority=0,
                 dont_filter=False, errback=None):

        self._encoding = encoding  # this one has to be set first
        self.method = str(method).upper()
        self._set_url(url)
        self._set_body(body)
        assert isinstance(priority, int), "Request priority not an integer: %r" % priority
        self.priority = priority

        assert callback or not errback, "Cannot use errback without a callback"
        self.callback = callback
        self.errback = errback

        self.cookies = cookies or {}
        self.headers = Headers(headers or {}, encoding=encoding)
        self.dont_filter = dont_filter

        self._meta = dict(meta) if meta else None
    
    @classmethod
    def request_fingerprint(cls,request, include_headers=None):
        """
        Return the request fingerprint.
        
        The request fingerprint is a hash that uniquely identifies the resource the
        request points to. For example, take the following two urls:
        
        http://www.example.com/query?id=111&cat=222
        http://www.example.com/query?cat=222&id=111
    
        """
        if include_headers:
            include_headers = tuple([h.lower() for h in sorted(include_headers)])
        fp = hashlib.sha1()
        fp.update(request.method)
        fp.update(canonicalize_url(request.url))
        fp.update(request.body or '')
        if include_headers:
            for hdr in include_headers:
                if hdr in request.headers:
                    fp.update(hdr)
                    for v in request.headers.getlist(hdr):
                        fp.update(v)
        return fp.hexdigest()
    @property
    def request_path(self):
        return Request.request_fingerprint(self)       

    @property
    def meta(self):
        if self._meta is None:
            self._meta = {}
        return self._meta

    def _get_url(self):
        return self._url

    def _set_url(self, url):
        if isinstance(url, str):
            self._url = escape_ajax(safe_url_string(url))
        elif isinstance(url, unicode):
            if self.encoding is None:
                raise TypeError('Cannot convert unicode url - %s has no encoding' %
                    type(self).__name__)
            self._set_url(url.encode(self.encoding))
        else:
            raise TypeError('Request url must be str or unicode, got %s:' % type(url).__name__)
        if ':' not in self._url:
            raise ValueError('Missing scheme in request url: %s' % self._url)

    url = property(_get_url, _set_url)

    def _get_body(self):
        return self._body

    def _set_body(self, body):
        if isinstance(body, str):
            self._body = body
        elif isinstance(body, unicode):
            if self.encoding is None:
                raise TypeError('Cannot convert unicode body - %s has no encoding' %
                    type(self).__name__)
            self._body = body.encode(self.encoding)
        elif body is None:
            self._body = ''
        else:
            raise TypeError("Request body must either str or unicode. Got: '%s'" % type(body).__name__)

    body = property(_get_body, _set_body )

    @property
    def encoding(self):
        return self._encoding

    def __str__(self):
        return "<%s %s>" % (self.method, self.url)

    __repr__ = __str__

    def copy(self):
        """Return a copy of this Request"""
        return self.replace()

    def replace(self, *args, **kwargs):
        """Create a new Request with the same attributes except for those
        given new values.
        """
        for x in ['url', 'method', 'headers', 'body', 'cookies', 'meta', \
                'encoding', 'priority', 'dont_filter', 'callback', 'errback']:
            kwargs.setdefault(x, getattr(self, x))
        cls = kwargs.pop('cls', self.__class__)
        return cls(*args, **kwargs)
