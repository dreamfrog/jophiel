'''
Created on 2012-5-11

@author: lzz
'''
from django.utils import unittest
from jophiel.crawler.http import Request
from .base import TaskSpider
from .tasks import fetchs_task
from .tasks import fetch_one_task

from .tables import RequestTable

class CrawlerTest(unittest.TestCase):
    
    def setUp(self):
        self.start_urls = [
                "http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html",
                "http://docs.python.org/library/traceback.html",
                "http://i.imgur.com/3C1ru.jpg",
                'http://pastebin.com/U0VzeCd0',
                'http://xlp223.ycool.com/post.497617.html',
             ]
        self.spider = TaskSpider("spider","request_table","page_storage",{})
        self.table = RequestTable(self.spider.tablename)
        for url in self.start_urls:
            request = Request(url)
            self.table.store_request(request)
        for value in self.table.select():
            print value

    def tearDown(self):
        for value in self.table.select():
            print value                    
    def testOneTask(self):
        for url in self.start_urls[:1]:
            request = Request(url)
            result = fetch_one_task.delay(self.spider,request)
            
    def testFetchsTask(self):
        fetchs_task.delay(self.spider)
        
        
    def testRequestTable(self):
        table = RequestTable("RequestTable")
        table.insert(request_path = "hhhhhh",url = "http://sbaidu.com_")
        where = {
                 "url" : "http://sbaidu.com_"
                 }
        #for value in  table.select(where):
        #    print value
    
        