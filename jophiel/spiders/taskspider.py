from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from .models import Task

class TaskSpider(CrawlSpider):
    '''
    TaskSpider is a base task oriented spider that other task spiders inherit from.
    '''
    
    def __init__(self,model):
        """Constructor takes care of loading task definition and compiling rules"""
        super(TaskSpider, self).__init__()
        self.model = model
    
    @classmethod
    def load(cls, task_name):
        '''
        Gets task for the spider, loads the tasks's module code and applies code
        from configuration to the spider.
        '''
        cls.name = task_name
        task = Task.objects.get(name = task_name)
        
        if task:
            urls = []
            if task.start_urls:
                urls = task.start_urls.splitlines()
            cls.start_urls = urls
            rules = []
            if task.rules:
                rule_texts = task.rules.splitlines()
                for item in rule_texts:
                    rule = Rule(SgmlLinkExtractor(allow=item), follow=True)
                    rules.append(rule)
            cls.rules = rules
            
            allowed_domains = []
            if task.allowed_domains:
                allowed_domains = task.allow_domains.splitlines()
            cls.allowed_domains = allowed_domains
        
        return cls(task)

