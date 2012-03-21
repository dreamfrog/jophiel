'''
Created on 2012-3-15

@author: lzz
'''
import uuid

from datetime import timedelta
from jophiel.utils import safe_str_to_class

class JobBase(object):
    def __init__(self,task_name,queue,*args, **kwargs):
        self.task_name = task_name
        self.queue = queue
        self.args = args
        self.kwargs = kwargs
        self.task_id = None
        self.task_id = uuid.uuid4().hex 