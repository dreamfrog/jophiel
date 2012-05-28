'''
Created on 2012-5-11

@author: lzz
'''
import json
from django.utils import unittest
from jophiel.crawler.http import Request

from .base import TaskSpider
from .models import Spider
from .tasks import fetchs_task
from .tasks import schedule_task
from .tasks import fetch_one_task

from .tables import RequestTable

class CrawlerTest(unittest.TestCase):
    
    def setUp(self):
        self.start_urls = [
                "http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html",
                "http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html",
                "http://httplib2.googlecode.com/hg/doc/html/index.html",
                "http://redis.io/commands/llen",
                "http://redis.io/clients",
                "http://redis.io/download",
                "http://redis.io/topics/memory-optimization",
                "http://redis.io/commands/rename",
                "http://redis.io/commands/pexpire",
                "http://redis.io/commands/expire",
                "http://redis.io/commands/restore",
                "http://redis.io/commands/dump",
                "http://redis.io/commands/exists",
                "http://redis.io/commands/ttl",                
             ]
        rules =[{
              "allow":"http://httplib2.googlecode.com/hg/.*$"
              },
             {
              "allow":"redis.io"
              }
             ]
        self.spider = TaskSpider(name = "spider",
                                         tablename="request_table",
                                         storagename="page_storage",setting={},
                                         rules = rules
                                         )
        self.spider.save_tasks()  
        self.table = RequestTable(self.spider.tablename)
        for url in self.start_urls:
            request = Request(url)
            self.table.store_request(request)

    def tearDown(self):
        #for value in self.table.iter_items():
        #    print value   
        pass   
    
    def Delay(self):
        urls = [
                "http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html",
                "http://httplib2.googlecode.com/hg/doc/html/index.html"
                ]
        for url in urls:
            request =  Request(url)
            fetch_one_task.push_domain_queue(request)
        count = fetch_one_task.get_domain_queue_count(request)
        self.assertEqual(count, 2)
        
        fetch_one_task.pop_domain_queue(request)
        delay = fetch_one_task.get_delay(request)
        count = fetch_one_task.get_domain_queue_count(request)    
        self.assertEqual(count,1)
        self.assertEqual(delay,None)
        
        urls_2 = [
                "http://redis.io/commands/llen",
                "http://redis.io/clients",
                "http://redis.io/download",
                "http://redis.io/topics/memory-optimization",
                ]
        for url in urls_2:
            request = Request(url)
            fetch_one_task.push_domain_queue(request)
        url = "http://redis.io/commands/psubscribe"
        request = Request(url)
        delay = fetch_one_task.get_delay(request)     
        self.assertEqual(delay, fetch_one_task.default_delay) 
        for url in urls_2:
            request = Request(url)
            fetch_one_task.pop_domain_queue(request)
        
    
    def PeriodTask(self):
        print "test-peroid"
        schedule_task.delay(self.spider.name) 
             
    def OneTask(self):
        for url in self.start_urls:
            request = Request(url)
            result = fetch_one_task.delay(self.spider,request)
            
    def testCreateTask(self):
        from .utils import create_spider_task
        from jophiel.models import IntervalSchedule
        from jophiel.models import PeriodicTask
        create_spider_task(self.spider)
        task  = PeriodicTask.objects.get(name = self.spider.name)
        from anyjson import deserialize, serialize
        import json
        for task in PeriodicTask.objects.all():

            print type(task.args)
            value  = "[\"spider\"]"
            print "----",task.args,task.kwargs
            print value == task.args
            #value = task.args+" "
            #print value,type(value)
            print json.loads(value)
            json.loads(task.args)
            json.loads(task.kwargs)
            
        
        
        
        
        
        
        
      