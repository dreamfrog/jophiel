'''
Created on 2012-3-23

@author: lzz
'''

from jophiel import app
from .message import MessageQueue
from jophiel.app import logger

class TaskQueue(MessageQueue):

    client = app.client
    
    @classmethod
    def enqueue_cls(cls,task):pass 
    
    @classmethod
    def enqueue(cls,taskinfo):
        queue = taskinfo.get('queue',None)
        if queue:
            cls.push(queue, taskinfo)
            logger.info("enqueued '%s' job on queue %s" % (str(taskinfo), queue))
        else:
            logger.error("unable to enqueue job with class %s" % str(taskinfo))

    @classmethod
    def dequeue(cls,queue):
        queue_name,taskinfo = cls.pop(queue)
        return taskinfo
