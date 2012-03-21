'''
Created on 2012-3-16

@author: lzz
'''

import time

from jophiel.tasks import async
from jophiel.backend.taskqueue import TaskQueue

from jophiel.app import logger

def perform(job):
    """Execute this task locally, by blocking until the task returns.
    """
    task_id = job.task_id
    task_name = job.task_name
    queue = job.queue
    args = job.args.copy()
    kwargs = job.kwargs.copy()
    result = async.async_task(task_id,task_name,queue,*args,**kwargs)
    return result

class Scheduler(object):

    def __init__(self, server="localhost:6379", password=None):
        self._shutdown = False
        self.resq = TaskQueue()

    @classmethod
    def run(cls, server, password=None):
        sched = cls(server=server, password=password)
        sched()
        
    def schedule_shutdown(self, signal, frame):
        logger.info('shutting down started')
        self._shutdown = True

    def __call__(self):
        logger.info('starting up')
        self.register_signal_handlers()
        #self.load_schedule()
        logger.info('looking for delayed items')
        while True:
            if self._shutdown:
                break
            self.handle_delayed_items()
            logger.debug('sleeping')
            time.sleep(5)
        logger.info('shutting down complete')

    def next_timestamp(self):
        while True:
            timestamp = self.resq.next_delayed_timestamp()
            if timestamp:
                yield timestamp
            else:
                break

    def next_item(self, timestamp):
        while True:
            item = self.resq.next_item_for_timestamp(timestamp)
            if item:
                yield item
            else:
                break

    def handle_delayed_items(self):
        for timestamp in self.next_timestamp():
            logger.info('handling timestamp: %s' % timestamp)
            for item in self.next_item(timestamp):
                logger.debug('queueing item %s' % item)
                klass = item['class']
                queue = item['queue']
                args = item['args']
                kwargs = {}
                if 'first_attempt' in item:
                    kwargs['first_attempt'] = item['first_attempt']
                #self.resq.enqueue_from_string(klass, queue, *args, **kwargs)
