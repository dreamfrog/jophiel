'''
Created on 2012-2-23

@author: lzz
'''

import unittest
from unittest import TestCase

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
