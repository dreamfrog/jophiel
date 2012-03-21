'''
Created on 2012-3-9

@author: lzz
'''

class states(object):
    SUCCESS = 0
    FAILURE = 1
    PENDING = 2
    RETRY = 3
    EXCEPTION_STATES = 4    

class TaskResult(object):
    def __init__(self,job,task_id,retval,status,traceback):
        self.job = job
        self.job_id = task_id
        self.retval = retval
        self.status = status
        self.traceback = traceback

class AsyncResult(object):
    def __init__(self,task_id,task=None):
        self.task_id = task_id
        self.task = task
