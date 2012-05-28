'''
Created on 2012-5-17

@author: lzz
'''
import copy
import json
from jophiel.crawler.spider import Spider
from jophiel.crawler.linkextractors.sgml import SgmlLinkExtractor
from . import models

"""
("allow","deny","allow_domains","deny_domains","restrict_xpaths"):
"""
class CrawlSpider(Spider):

    def __init__(self, *a, **kw):
        super(CrawlSpider, self).__init__(*a, **kw)
        self._rules = []
        self.rules = kw["rules"] if "rules" in kw else []
        self.domains = kw["domains"] if "domains" in kw else []

            
    def append_rule(self,rule):
        self._compile_rule(rule)
        
    def _compile_rules(self):
        for rule in self.rules:
            self.append_rule(rule)  
                 
    def _compile_rule(self,rule):
        _rule = SgmlLinkExtractor(**rule)
        self._rules.append(_rule)
    
    def extract_links(self,response):
        links = []
        if not self._rules:
            self._compile_rules()
        for rule in self._rules:
            link_ = rule.extract_links(response)
            links.extend(link_)
        return links
                
from .models import Spider

class TaskSpider(CrawlSpider):
    
    def __init__(self,name,settings={},**kwargs):
        super(TaskSpider,self).__init__(name,settings,**kwargs)
        self.tablename = kwargs["tablename"] if "tablename" in kwargs else name
        self.storagename = kwargs["storagename"] if "storagename" in kwargs else name
        
    def save_tasks(self):
        try:
            obj = models.Spider.objects.get(name=self.name)
        except models.Spider.DoesNotExist:
            obj = models.Spider(
                   name = self.name,
                   rules = json.dumps(self.rules),
                   tablename = self.tablename,
                   storagename = self.storagename,
                   settings = json.dumps(self.settings),
                   domains = json.dumps(self.domains)
            )
            obj.save()
            
    @classmethod
    def load_tasks(cls,name):
        model = models.Spider.objects.get(name= name)
        task = cls(name,
                   settings = json.loads(model.settings),
                   rules = json.loads(model.rules),
                   tablename = model.tablename,
                   storagename = model.storagename,
                   domains = json.loads(model.domains)
                   )
        return task
    
        
        
    
        