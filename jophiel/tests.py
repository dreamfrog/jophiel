'''
Created on 2012-2-28

@author: lzz
'''

import unittest
from unittest import TestCase
from jophiel.db.models import BaseModel
from jophiel.db.field import *
import random 

class HttpRequestSchema(BaseModel):
    
    row_key = KeyField()
    
    url = StringField()
    last_modify_time = DateTimeField()
    body = StringField()
    

class TestModel(TestCase):
    
    def setUp(self):
        self.table_name = "fantong"
        HttpRequestSchema.objects.create_schema(self.table_name)
        
    def setDown(self):pass
    
    def testBasicSaveGet(self):pass
        
    def testBasicGet(self):
        url = "http://www.dianping.com/shop/223223.html"
        request = HttpRequestSchema(self.table_name,url)
        request.url = url
        request.body = "dianping"
        request.save()
        
        model = HttpRequestSchema.objects.get(self.table_name,url)
        
        self.assertEqual(model.url,request.url,"error in field url")
        self.assertEqual(model.last_modify_time ,request.last_modify_time,"error in last modified field")
        
    def testMutiGet(self):
        url_1 = "http://111.com"
        request1 = HttpRequestSchema(self.table_name,url_1)
        request1.url = url_1
        request1.body = "111"
        request1.save()
        
        url = "http://222.com"
        request = HttpRequestSchema(self.table_name,url)
        request.url = url
        request.body = "222"
        request.save()
                
        model = HttpRequestSchema.objects.get(self.table_name,url_1)
        assert model.url==request1.url ,"error in field url %s ---%s "%(model.url,request.url)
        assert model.body == request1.body
        assert model.last_modify_time == request1.last_modify_time,"error in last modified field"        
   
class TestQueue(TestCase):
    
    def setUp(self):
        from jophiel.taskqueue import RedisQueue
        self.tasks = RedisQueue()
        
    def setDown(self):pass
    
    def testEnqueue(self):
        queue = "redis"
        params = {
                  "__class___":"message_queue"
                  }
        self.tasks.remove_queue(queue)
        self.tasks.push(queue, params)
        assert self.tasks.queues() == set(['redis']), "error in queues"
        task = self.tasks.pop(queue)
        assert task == (queue, params), "error in dequeue tasks" 
        assert self.tasks.size(queue) == 0, "erroy in remove queue"

     

if __name__=="__main__":
    unittest.main()