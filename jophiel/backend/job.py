'''
Created on 2012-3-12

@author: lzz
'''

"""
    resque:jobs  -- [job_name,]
    resque:job_name:
    resque:job_name:params
    resque:job_name:tasks
    resque:job_name:queue
    resque:job_name:schedule
    
"""

from jophiel.backend.base import BaseStat
from jophiel.app import logger

class JobStats(BaseStat):
    resq_params = ""
    
    def __init__(self,job_name):
        self.job_name = job_name
        
    