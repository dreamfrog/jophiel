'''
Created on 2012-3-12

@author: lzz
'''

import time
import datetime
import json
import uuid

from jophiel.app import client
from jophiel.backend.base import BaseStat
from jophiel.backend import count
from jophiel.app import logger


"""
    /*need clean task information*/
    
    resque:tasks:task_id:status
    resque:tasks:task_id:params --hash
    resque:tasks:task_id:name --str
    resque:tasks:task_id:start --str
    resque:tasks:task_id:end --str
    resque:tasks:task_id:stats --hash
    resque:tasks:task_id:worker_id  --str
    resque:tasks:task_id:queue
    resque:tasks:
    
    apply (queue,task_name,params)
        --generate task_id
        --register task
        --update status  --pending
        --send_task -------------------------- worker
                                             ----pull task 
                                             ----update task status   --working 
                                             ----fill worker_id,start_time,
                                             ----processing
                                             -----update task status
                                             _____end processing
                                             -----update end time 
                                             -----update status  ---processed
  get async_result(task_id)
      ---,task_id
"""
class TaskStat:
    pending = "pending"
    processing = "working"
    processed = "processed"

class TaskStats(BaseStat):
    
    resq_tasks = "resque:tasks"
    resq_params = "resque:tasks:%s:params"
    resq_name = "resque:tasks:%s:name"
    resq_start = "resque:tasks:%s:start"
    resq_end = "resque:tasks:%s:end"
    resq_stats = "resque:tasks:%s:stats"
    resq_workerid = "resque:tasks:%s:worker_id"
    resq_queue = "resque:tasks:%s:queue"
    resq_status = "resque:tasks:%s:status"
     
    def __init__(self,queue,params,task_name,task_id = None,):
        self.task_id =task_id
        if not task_id:
            self.worker_id = uuid.uuid4().hex
        self.queue = queue
        self.params = params
        self.task_name = task_name
    
    def __str__(self):
        return "%s"%self.worker_id
  
    @classmethod
    def from_task_id(cls,task_id):
        if client.sismember(cls.resq_tasks,task_id):
            queue = client.get(cls.resq_queue%task_id)
            params = client.get(cls.resq_params%task_id)
            task_name = client.get(cls.resq_name%task_id)
            obj = cls(queue,params,task_name,task_id)
            return obj
        else:
            return None 
 
    """    
        get or set task start time or end time
    """   
    def _set_started(self, dt):
        if dt:
            value = int(time.mktime(dt.timetuple()))
            client.set(self.resq_start% self, value)
        else:
            client.delete(self.resq_start% self)

    def _get_started(self):
        datestring = client.get(self.resq_start%self)
        return datestring
    started = property(_get_started, _set_started)
 
    def _set_end(self, dt):
        if dt:
            value = int(time.mktime(dt.timetuple()))
            client.set(self.resq_end%self, value)
        else:
            client.delete(self.resq_end % self)
    def _get_end(self):
        datestring = client.get(self.resq_end % self)
        return datestring
    
    started = property(_get_started, _set_started)
    
    """
        get or update task stat
    """
    def update_stat(self,key,value):
        client.hset(self.resq_stats%self.task_id, key, value)        
    def get_stat(self,key):
        return client.hget(self.resq_stats%self.task_id, key)
    def get_stats(self):
        return client.hgetall(self.resq_stats%self.task_id)
 
    """
        register task info
    """   
    def register(self):
        client.sadd(self.resq_tasks, str(self))
        client.set(self.resq_queue%self.task_id,self.queue)
        client.set(self.resq_name%self.task_id,self.task_name)
        client.set(self.resq_params%self.task_id,self.params)
        self.started = datetime.datetime.now()
        
    def unregister(self):
        client.srem(self.resq_tasks, str(self))
        self.started = None
    
    def update_status(self,status):
        client.set(self.resq_status%self.task_id,status)  