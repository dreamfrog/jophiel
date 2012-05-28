'''
Created on 2012-5-11

@author: lzz
'''

from django.utils import unittest
from .spider import Spider
from .download import Downloader
from . import conf
from .http.request import Request
from jophiel.tasks import serialize


class CrawlerTest(unittest.TestCase):
    
    def setUp(self):
        self.start_urls = [
                "http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html",
                "http://docs.python.org/library/traceback.html",
                "http://i.imgur.com/3C1ru.jpg"
             ]
    
    def testCrawler(self):
        setting = {}
        spider = Spider("spider",setting)
        downloader = Downloader(conf)
        request = Request("http://www.baidu.com")
        response = downloader.fetch(request,spider)
        
    
    def testWebPage(self):
        setting = {}
        url = 'http://hbase.apache.org/book.html'
        spider = Spider("spider",setting)
        downloader = Downloader(conf)
        for url in self.start_urls:
            request = Request(url)
            response = downloader.fetch(request,spider)  

              
        