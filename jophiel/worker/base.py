'''
Created on 2012-3-1

@author: lzz
'''

import sys
import uuid
import time

from jophiel import app
from jophiel.errors import NotImplementError
from jophiel.monitor.worker import WorkerStats
from jophiel.queues.task import TaskQueue
from jophiel.tasks.utils import build_task
from jophiel.tasks import engine 
from jophiel.app import logger

def processsing(func):
    def new_func(self,taskinfo,*args, **argkw):
        worker = WorkerStats(self.worker_id,self.queue)
        task = None
        try:
            task = build_task(taskinfo)
            worker.working_on(task)
            if hasattr(self,"before_worker"):
                self.before_worker(self,task)
            return func(self,task,*args, **argkw)
        except Exception, e:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            logger.exception("%s failed: %s" % (task))
            if hasattr(self,"worker_failed"):
                self.worker_failed(self,task)
            worker.failed()
        else:
            logger.info('completed job details: %s'%task)
            if hasattr(self,"worker_success"):
                self.worker_success(self,task)           
        finally:
            if hasattr(self,"after_worker"):
                self.after_worker(self,task)               
            worker.done_working()
    return new_func 
            
def register(func):
    def new_func(self,task,*args,**argws):
        worker = WorkerStats(self.worker_id,self.queue)
        worker.register_worker()
        return func(self,task,*args,**argws)
    return new_func 

def deregister(func):
    def new_func(self,task,*args,**argws):
        worker = WorkerStats(self.worker_id,self.queue)
        worker.unregister_worker()
        return func(self,task,*args,**argws)            
    return new_func 
def running(func):
    def new_func(self,task,*args,**argws):
        if hasattr(self,"startup"):
            self.startup()
        try:
            func(self,*args,**argws)            
        except:
            pass
        finally:
            if hasattr(self,"stop"):
                self.stop()
    return new_func 

class BasicWorker(object):
    def __init__(self,queue,worker_id=None,*args,**argv):
        self.queue = queue
        self.worker_id= worker_id
        self.running = False
        if not worker_id:
            self.worker_id = uuid.uuid4().hex

    def next_task(self,interval = 0):
        taskinfo = TaskQueue.dequeue(self.queue)
        return taskinfo
    
    @processsing    
    def process(self, task):
        return task.perform()
    @register
    def startup(self):pass
    @deregister
    def stop(self):pass
    
    def schedule_down(self):
        self.running = False
        
    @running
    def start(self):
        self.runnging = True
        self.work()

    @classmethod
    def run(cls, queue):
        worker = cls(queues=queue)
        worker.start()
 
    def work(self):
        raise NotImplementError("please implement work method")

class Worker(BasicWorker):
    def __init__(self, queue,internal = 0):
        super(Worker,self).__init__(queue)
        self.internal = internal
        
    def prcocess_task(self,task):
        engine.perform(task)
        
    def work(self):
        while True:
            if not self.running:
                logger.info('shutdown scheduled:to stop worker %s ',self.worker_id)
                break
            
            if self.internal:
                time.sleep(self.internal)
            taskinfo = self.next_task()
            if taskinfo:
                self.process_task(taskinfo)   
                 
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-q", dest="queue_name")
    (options, args) = parser.parse_args()
    if not options.queue_name:
        parser.print_help()
        parser.error("Please give each worker at least one queue.")
    queue = options.queue_name
    Worker.run(queue)      