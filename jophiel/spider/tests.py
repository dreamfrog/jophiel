'''
Created on 2012-5-11

@author: lzz
'''
from django.utils import unittest
from jophiel.crawler.http import Request
from .base import TaskSpider
from .tasks import fetch_task

from .tables import RequestTable

class CrawlerTest(unittest.TestCase):
    
    def setUp(self):
        self.start_urls = [
                "http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html",
                "http://docs.python.org/library/traceback.html",
                "http://i.imgur.com/3C1ru.jpg"
             ]
            
    def testTask(self):
        spider = TaskSpider("spider",{})
        for url in self.start_urls:
            request = Request(url)
            result = fetch_task.delay(request,spider)
            resp = result.wait()
            print resp.headers
            print resp.flags
            
    def testRequestTable(self):
        table = RequestTable("RequestTable")
        table.insert(request_path = "hhhhhh",url = "http://sbaidu.com_")
        where = {
                 "url" : "http://sbaidu.com_"
                 }
        for value in  table.select(where):
            print value
        