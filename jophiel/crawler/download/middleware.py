"""
Downloader Middleware manager

See documentation in docs/topics/downloader-middleware.rst
"""
from collections import defaultdict

from ..http import Request, Response

class DownloaderMiddlewareManager(object):

    def __init__(self, *middlewares):
        self.middlewares = middlewares
        self.methods = defaultdict(list)
        for mw in middlewares:
            self._add_middleware(mw)

    def _add_middleware(self, mw):
        if hasattr(mw, 'process_request'):
            self.methods['process_request'].append(mw.process_request)
        if hasattr(mw, 'process_response'):
            self.methods['process_response'].insert(0, mw.process_response)
        if hasattr(mw, 'process_exception'):
            self.methods['process_exception'].insert(0, mw.process_exception)

    def download(self, download_func, request, spider):
        def process_request(request):
            for method in self.methods['process_request']:
                response = method(request=request, spider=spider)
                assert response is None or isinstance(response, (Response, Request)), \
                        'Middleware %s.process_request must return None, Response or Request, got %s' % \
                        (method.im_self.__class__.__name__, response.__class__.__name__)
                if response:
                    return response
            return None

        def process_response(response):
            assert response is not None, 'Received None in process_response'
            if isinstance(response, Request):
                return response

            for method in self.methods['process_response']:
                response = method(request=request, response=response, spider=spider)
                assert isinstance(response, (Response, Request)), \
                    'Middleware %s.process_response must return Response or Request, got %s' % \
                    (method.im_self.__class__.__name__, type(response))
                if isinstance(response, Request):
                    return response
            return response

        def process_exception(exception):
            for method in self.methods['process_exception']:
                response = method(request=request, exception=exception, spider=spider)
                assert response is None or isinstance(response, (Response, Request)), \
                    'Middleware %s.process_exception must return None, Response or Request, got %s' % \
                    (method.im_self.__class__.__name__, type(response))
                if response:
                    return response
            return exception
            
        try:
            response = process_request(request)
            if response and isinstance(response,Response):
                return response
            else:
                response = download_func(request=request, spider=spider)
                return process_response(response)
        except  Exception, e:
            return process_exception(e)
