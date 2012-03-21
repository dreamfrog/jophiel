'''
Created on 2012-3-12

@author: lzz
'''
from jophiel.tasks.base import Task

class TestTask(Task):
    
    name = "test"

    def run(self, *args, **kwargs):
        print "hello,scrapy"
        
    def execute(self, **kwargs):
        print "hello,scrapy"
        pass
    