'''
Created on 2012-3-1

@author: lzz
'''

import logging
import signal
import sys
import uuid

from jophiel.backend.worker import WorkerStats
from jophiel.backend.taskqueue import TaskQueue
from jophiel import app

logger = logging.getLogger(__name__)

class BasicWorker(object):
    
    def __init__(self,queue,*args,**argv):
        self.child = None
        self.worker_id = uuid.uuid4().hex
        self.worker = WorkerStats(self.worker_id,queue)
        self.queue = queue
    
    def get_worker_id(self):
        return self.worker_id    
    
    def before_process(self, job):
        return job
    
    def build_task(self,taskinfo):
        task_name = taskinfo["task_name"]
        task_id = taskinfo["task_id"]
        args = "args"
        kwargs = "kwargs"
        task = app.tasks[task_name]
        return task(task_name,task_id,args,kwargs)
            
    def next_task(self,interval = 0):
        taskinfo = TaskQueue.dequeue(self.queue)
        task = None
        if taskinfo:
            task = self.build_task(taskinfo)
        return task
        
    def process(self, task=None):
        try:
            self.worker.working_on(task)
            job = self.before_process(task)
            return task.perform()
        
        except Exception, e:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            logger.exception("%s failed: %s" % (job, e))
            task.fail(exceptionTraceback)
            self.worker.failed()
        else:
            logger.info('completed job details: %s'%job)

        finally:
            self.worker.done_working()

    def startup(self):
        self.worker.register_worker()

    def stop(self):
        self.worker.unregister_worker()
    
    def work(self):
        pass
    
    @classmethod
    def run(cls, queues):
        worker = cls(queues=queues)
        worker.startup()
        try:
            worker.work()
        except:
            pass
        finally:
            worker.stop()
                