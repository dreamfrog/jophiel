'''
Created on 2012-3-21

@author: lzz
'''
from jophiel import app

def build_task(self,taskinfo):
    task_name = taskinfo["task_name"]
    task_id = taskinfo["task_id"]
    args = taskinfo["args"]
    kwargs = taskinfo["kwargs"]
    task = app.tasks[task_name](task_id,*args,**kwargs)
    return task

def package_task(self,task):
    taskinfo = {
       "task_id":task.task_id,
       "task_name":task.task_name,
       "args":task.args,
       "kwargs":task.kwargs,
       "queue":task.queue
       }
    return taskinfo
