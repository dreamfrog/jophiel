'''
Created on 2012-5-3

@author: lzz
'''

from .base import BaseProcessor
from ..linkextractors.image import HTMLImageLinkExtractor

class ImageLinkExtractor(BaseProcessor):
    def __init__(self,allow = (),deny=(),location=()):
        self.extractor = HTMLImageLinkExtractor(location)
        
    def process_item(self, request,response, spider):
        return self.extractor.extract_links(response)
    