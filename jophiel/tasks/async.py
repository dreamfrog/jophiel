'''
Created on 2012-3-21

@author: lzz
'''

from jophiel.tasks.utils import package_task
from jophiel import app
from jophiel.queues.task import TaskQueue
from jophiel.tasks import AsyncResult

"""    
    async method process
"""
def async_task(task_id,task_name,queue,*args,**kwargs):
    taskcls = app.tasks[task_name]
    task = taskcls(task_id,*args,**kwargs)
    taskinfo = package_task(task)
    TaskQueue.enqueue(taskinfo)
    return AsyncResult(task_id,task)   
    