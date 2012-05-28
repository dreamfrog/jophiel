'''
Created on 2012-5-3

@author: lzz
'''

from ..http.request import Request

class ProcessorManager(object):

    def __init__(self, processors = []):
        self.processors = processors
    
    """need do some processor for this method"""
    def _build_request(self,link,request,response,spider):
        return Request(url = link.rul)
        
    def process_item(self, request,response, spider):
        links = []
        for processor in self.processors:
            items = processor.process_item(request,response,spider)
            if items:
                links.extend(items)
        requests = []
        for link in links:
            if isinstance(link,Request):
                requests.append(link)
            else:
                request = self._build_request(link, request, response, spider)
                requests.append(request)
                