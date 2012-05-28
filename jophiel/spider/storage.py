'''
Created on 2012-5-18

@author: lzz
'''

from jophiel.crawler.storage import WebPage

class PageStorage(WebPage):
    
    @classmethod
    def storage_page(cls,spider,request,response):
        storage = WebPage(spider.storagename)
        storage.store_response(spider, request, response)