'''
Created on 2012-3-12

@author: lzz
'''
from jophiel.tasks.base import Task

class TestTask(Task):
    
    name = "test"
    
    def execute(self, request, **kwargs):
        print "hello,scrapy"
        pass
    