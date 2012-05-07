'''
Created on 2012-5-2

@author: lzz
'''
from celery.task.base import Task
from celery.task.sets import TaskSet

import redis

class CommonTask(Task):
    abstract = True

    def after_return(self, *args, **kwargs):
        print("Task returned: %r" % (self.request, ))
        

class RedisTask(Task):
    abstract = True
    _db = None
    
    @property
    def db(self):
        if self._db ==None:
            self._db = redis.client
        return self._db
    
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print("Task returned: %r" % (self.request, ))
        
