'''
Created on 2012-4-29

@author: lzz
'''
from celery.task.base import Task
from celery.task.sets import TaskSet

import redis

class DebugTask(Task):
    abstract = True

class RedisTask(Task):
    _db = None
    
    @property
    def db(self):
        if self._db ==None:
            self._db = redis.client
        return self._db
    
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        print("Task returned: %r" % (self.request, ))
        
"""
from celery.execute import send_task
result = send_task("tasks.add", [2, 2])
result.get()
"""