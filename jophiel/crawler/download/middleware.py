"""
Downloader Middleware manager

See documentation in docs/topics/downloader-middleware.rst
"""
from collections import defaultdict
from jophiel.crawler.http import Request, Response
from jophiel.crawler import conf
from jophiel.crawler.utils.conf import build_component_list
from jophiel.crawler.utils.misc import load_object

class DownloaderMiddlewareManager(object):

    def __init__(self):
        self.methods = defaultdict(list)
        self.middlewares =[]     
        for clspath in build_component_list(conf.DOWNLOAD_MIDDLEWARES,{}):
            mwcls = load_object(clspath)
            self.middlewares.append(mwcls)
            self._add_middleware(mwcls)

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
            import traceback
            import sys
            traceback.print_exc(file=sys.stdout)
            return process_exception(e)
