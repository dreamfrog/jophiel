'''
Created on 2012-5-17

@author: lzz
'''

from jophiel.crawler.spider import Spider

class TaskSpider(Spider):
    
    def __init__(self,name,tablename,storagename,setting={},**kwargs):
        super(TaskSpider,self).__init__(name,setting,**kwargs)
        self.tablename = tablename
        self.storagename = storagename