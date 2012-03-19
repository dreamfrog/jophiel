'''
Created on 2012-3-6

@author: lzz
'''

import calendar
import email.utils
import httplib
import time
import weakref

import httputil
from escape import utf8

class HTTPRequest(object):
    """HTTP client request object."""
    def __init__(self, url, method="GET", headers=None, body=None,
                 auth_username=None, auth_password=None,
                 connect_timeout=20.0, request_timeout=20.0,
                 if_modified_since=None, follow_redirects=True,
                 max_redirects=5, user_agent=None, use_gzip=True,
                 network_interface=None, streaming_callback=None,
                 header_callback=None, prepare_curl_callback=None,
                 proxy_host=None, proxy_port=None, proxy_username=None,
                 proxy_password='', allow_nonstandard_methods=False,
                 validate_cert=True, ca_certs=None,
                 allow_ipv6=None,
                 client_key=None, client_cert=None):
        """Creates an `HTTPRequest`.

        All parameters except `url` are optional.

        :arg string url: URL to fetch
        :arg string method: HTTP method, e.g. "GET" or "POST"
        :arg headers: Additional HTTP headers to pass on the request
        :type headers: `~tornado.httputil.HTTPHeaders` or `dict`
        :arg string auth_username: Username for HTTP "Basic" authentication
        :arg string auth_password: Password for HTTP "Basic" authentication
        :arg float connect_timeout: Timeout for initial connection in seconds
        :arg float request_timeout: Timeout for entire request in seconds
        :arg datetime if_modified_since: Timestamp for ``If-Modified-Since``
           header
        :arg bool follow_redirects: Should redirects be followed automatically
           or return the 3xx response?
        :arg int max_redirects: Limit for `follow_redirects`
        :arg string user_agent: String to send as ``User-Agent`` header
        :arg bool use_gzip: Request gzip encoding from the server
        :arg string network_interface: Network interface to use for request
        :arg callable streaming_callback: If set, `streaming_callback` will
           be run with each chunk of data as it is received, and 
           `~HTTPResponse.body` and `~HTTPResponse.buffer` will be empty in 
           the final response.
        :arg callable header_callback: If set, `header_callback` will
           be run with each header line as it is received, and 
           `~HTTPResponse.headers` will be empty in the final response.
        :arg callable prepare_curl_callback: If set, will be called with
           a `pycurl.Curl` object to allow the application to make additional
           `setopt` calls.
        :arg string proxy_host: HTTP proxy hostname.  To use proxies, 
           `proxy_host` and `proxy_port` must be set; `proxy_username` and 
           `proxy_pass` are optional.  Proxies are currently only support 
           with `curl_httpclient`.
        :arg int proxy_port: HTTP proxy port
        :arg string proxy_username: HTTP proxy username
        :arg string proxy_password: HTTP proxy password
        :arg bool allow_nonstandard_methods: Allow unknown values for `method` 
           argument?
        :arg bool validate_cert: For HTTPS requests, validate the server's
           certificate?
        :arg string ca_certs: filename of CA certificates in PEM format,
           or None to use defaults.  Note that in `curl_httpclient`, if
           any request uses a custom `ca_certs` file, they all must (they
           don't have to all use the same `ca_certs`, but it's not possible
           to mix requests with ca_certs and requests that use the defaults.
        :arg bool allow_ipv6: Use IPv6 when available?  Default is false in 
           `simple_httpclient` and true in `curl_httpclient`
        :arg string client_key: Filename for client SSL key, if any
        :arg string client_cert: Filename for client SSL certificate, if any
        """
        if headers is None:
            headers = httputil.HTTPHeaders()
        if if_modified_since:
            timestamp = calendar.timegm(if_modified_since.utctimetuple())
            headers["If-Modified-Since"] = email.utils.formatdate(
                timestamp, localtime=False, usegmt=True)
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_username = proxy_username
        self.proxy_password = proxy_password
        self.url = url
        self.method = method
        self.headers = headers
        self.body = utf8(body)
        self.auth_username = auth_username
        self.auth_password = auth_password
        self.connect_timeout = connect_timeout
        self.request_timeout = request_timeout
        self.follow_redirects = follow_redirects
        self.max_redirects = max_redirects
        self.user_agent = user_agent
        self.use_gzip = use_gzip
        self.network_interface = network_interface
        self.streaming_callback = streaming_callback
        self.header_callback = header_callback
        self.prepare_curl_callback = prepare_curl_callback
        self.allow_nonstandard_methods = allow_nonstandard_methods
        self.validate_cert = validate_cert
        self.ca_certs = ca_certs
        self.allow_ipv6 = allow_ipv6
        self.client_key = client_key
        self.client_cert = client_cert
        self.start_time = time.time()


class HTTPResponse(object):
    """HTTP Response object.

    Attributes:

    * request: HTTPRequest object

    * code: numeric HTTP status code, e.g. 200 or 404

    * headers: httputil.HTTPHeaders object

    * buffer: cStringIO object for response body

    * body: respose body as string (created on demand from self.buffer)

    * error: Exception object, if any

    * request_time: seconds from request start to finish

    * time_info: dictionary of diagnostic timing information from the request.
        Available data are subject to change, but currently uses timings
        available from http://curl.haxx.se/libcurl/c/curl_easy_getinfo.html,
        plus 'queue', which is the delay (if any) introduced by waiting for
        a slot under AsyncHTTPClient's max_clients setting.
    """
    def __init__(self, request, code, headers={}, buffer=None,
                 effective_url=None, error=None, request_time=None,
                 time_info={}):
        self.request = request
        self.code = code
        self.headers = headers
        self.buffer = buffer
        self._body = None
        if effective_url is None:
            self.effective_url = request.url
        else:
            self.effective_url = effective_url
        if error is None:
            if self.code < 200 or self.code >= 300:
                self.error = HTTPError(self.code, response=self)
            else:
                self.error = None
        else:
            self.error = error
        self.request_time = request_time
        self.time_info = time_info

    def _get_body(self):
        if self.buffer is None:
            return None
        elif self._body is None:
            self._body = self.buffer.getvalue()

        return self._body

    body = property(_get_body)

    def rethrow(self):
        """If there was an error on the request, raise an `HTTPError`."""
        if self.error:
            raise self.error

    def __repr__(self):
        args = ",".join("%s=%r" % i for i in self.__dict__.iteritems())
        return "%s(%s)" % (self.__class__.__name__, args)


class HTTPError(Exception):
    """Exception thrown for an unsuccessful HTTP request.

    Attributes:

    code - HTTP error integer error code, e.g. 404.  Error code 599 is
           used when no HTTP response was received, e.g. for a timeout.

    response - HTTPResponse object, if any.

    Note that if follow_redirects is False, redirects become HTTPErrors,
    and you can look at error.response.headers['Location'] to see the
    destination of the redirect.
    """
    def __init__(self, code, message=None, response=None):
        self.code = code
        message = message or httplib.responses.get(code, "Unknown")
        self.response = response
        Exception.__init__(self, "HTTP %d: %s" % (self.code, message))
