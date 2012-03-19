'''
Created on 2012-3-15

@author: lzz
'''

from datetime import timedelta
from jophiel.utils import safe_str_to_class

class JobBase(object):
    
    def __init__(self,task_name,queue,args=[],opions={}):
        self.task_name = task_name
        self.queue = queue
        self.args = args
        self.options = opions
        self.task_id = None
        