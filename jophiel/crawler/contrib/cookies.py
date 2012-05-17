import os
from collections import defaultdict
from jophiel.crawler.xlib.pydispatch import dispatcher

from jophiel.crawler.exceptions import NotConfigured
from jophiel.crawler.http import Response
from jophiel.crawler.http.cookies import CookieJar

class CookiesMiddleware(object):

    jars =  defaultdict(CookieJar)

    @classmethod
    def process_request(cls, request, spider):
        if 'dont_merge_cookies' in request.meta:
            return

        jar = cls.jars[spider]
        cookies = cls._get_request_cookies(jar, request)
        for cookie in cookies:
            jar.set_cookie_if_ok(cookie, request)

        # set Cookie header
        request.headers.pop('Cookie', None)
        jar.add_cookie_header(request)

    def process_response(self, request, response, spider):
        if 'dont_merge_cookies' in request.meta:
            return response

        # extract cookies from Set-Cookie and drop invalid/expired cookies
        jar = self.jars[spider]
        jar.extract_cookies(response, request)
        self._debug_set_cookie(response, spider)

        return response

    def _get_request_cookies(self, jar, request):
        headers = {'Set-Cookie': ['%s=%s;' % (k, v) for k, v in request.cookies.iteritems()]}
        response = Response(request.url, headers=headers)
        cookies = jar.make_cookies(response, request)
        return cookies


