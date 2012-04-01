'''
Created on 2012-3-23

@author: lzz
'''

from .message import SimpleMessageQueue
from jophiel.tasks.utils import package_task
from jophiel.app import logger

class TaskQueue(SimpleMessageQueue):
    def __init__(self,queue):
        super(TaskQueue,self).__init__(queue)
        
    def enqueue_cls(self,task):
        taskinfo = package_task(task)
        self.enqueue(taskinfo)

    def enqueue(self,taskinfo):
        self.push(taskinfo)

    def dequeue(self):
        taskinfo = self.pop()
        return taskinfo
