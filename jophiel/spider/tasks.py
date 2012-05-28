'''
Created on 2012-5-2

@author: lzz
'''
from urlparse import urlparse

from celery.task import task
from celery.task import subtask
from celery.task.base import Task
from jophiel.crawler.http import Response
from jophiel.crawler.http import Request
from jophiel.crawler.download import Downloader
from jophiel.crawler.storage import WebPage
from jophiel.crawler.w3lib.http import headers_dict_to_raw,headers_raw_to_dict
from jophiel.crawler.http import Headers
from jophiel.storage import redis

from .tables import RequestTable
from .tables import RequestStat
from .storage import PageStorage
from .models import Spider
from .base import TaskSpider

class DownloaderTask(Task):
    _downloader = None 
    _redis = None  
    abstract = True
    max_requests = 3
    default_delay = 10
    default_limit = 10
    domain_prefix = "domains::"
    spider_prefix = "spiider::"
    
    @property
    def downloader(self):
        if not self._downloader:
            self._downloader = Downloader()
        return self._downloader
    
    @property
    def cache(self):
        if self._redis ==None:
            self._redis = redis.RedisBackend()
        return self._redis
    
    def get_domain_key(self,request):
        key = urlparse(request.url).hostname or ''
        return self.domain_prefix+key
    
    def get_spider_key(self,spider):
        return self.spider_prefix + spider.name
        
    def get_delay(self,request):
        key = self.get_domain_key(request)
        requests = self.cache.client.scard(key)
        if requests> self.max_requests:
            return self.default_delay
        return None
    
    def count_set_(self,key):
        return self.cache.client.scard(key)
    def push_set_(self,key,value):
        self.cache.client.sadd(key,value)
        
    def pop_set_(self,key,value):
        self.cache.client.srem(key,value) 
    
    def get_domain_queue_count(self,request):
        key = self.get_domain_key(request)
        return self.count_set_(key)       
     
    def push_domain_queue(self,request):
        key = self.get_domain_key(request)
        self.push_set_(key,request.request_path)
        
    def pop_domain_queue(self,request):
        key = self.get_domain_key(request)
        self.pop_set_(key, request.request_path)

    def push_spider_queue(self,spider,request):
        key = self.get_spider_key(spider)
        self.push_set_(key, request.request_path)
        
    def pop_spider_queue(self,spider,request):
        key = self.get_spider_key(spider)
        self.pop_set_(key,request.request_path)
        
    def get_spider_queue_count(self,spider):
        key = self.get_spider_key(spider)
        return self.count_set_(key)
    
    def request_is_member(self,spider,request):
        key = self.get_spider_key(spider)
        return self.cache.client.sismember(key,request.request_path)
        
    def after_return(self, *args, **kwargs):pass
    
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        print "tasks---",task_id,args,einfo
        
    def on_success(self, retval, task_id, args, kwargs):pass    


def link_extract_task(spider,response): 
    storage = RequestTable(spider.tablename)
    for link in spider.extract_links(response):
        try:
            request = Request(url=  link.url)
            storage.store_request(request)  
        except:
            pass  
        
@task(base=DownloaderTask,name="tasks.fetch_request",ignore_result=True)
def fetch_one_task(spider,request,callback=link_extract_task,default_retry_delay=30):
    delay = fetch_one_task.get_delay(request)
    if delay:
        max_retries=30
        retries = fetch_one_task.request.retries
        #clean
        if retries >=fetch_one_task.max_retries-1 or retries>max_retries:
            fetch_one_task.pop_spider_queue(spider,request)
            return 
        else:
            return fetch_one_task.retry(max_retries =  max_retries)
    
    try:
        fetch_one_task.push_domain_queue(request)
        response = fetch_one_task.downloader.fetch(request,spider) 
        if isinstance(response,Response):
            RequestTable.storage_response(spider,request,response)
            PageStorage.storage_page(spider, request, response)
            if callback:
                callback(spider,response)
    finally:
        fetch_one_task.pop_domain_queue(request)
        fetch_one_task.pop_spider_queue(spider,request)

@task(base = DownloaderTask,name="tasks.fetch_spiders",ignore_result=True)
def fetchs_task(spider,callback=fetch_one_task):
    table = RequestTable(spider.tablename)
    count = fetchs_task.get_spider_queue_count(spider)
    if count>10:
        return 
    for request in table.iter_requests(stat = RequestStat.STAT_NEED_DOWNLOAD,limit=fetchs_task.default_limit):
        if not fetchs_task.request_is_member(spider,request):
            fetch_one_task.push_spider_queue(spider,request)
            fetch_one_task.apply_async(args=(spider,request))

@task(base = DownloaderTask,name="tasks.schedule_spider_task")
def schedule_task(name,callback=fetchs_task):
    print "fetch-task %s"%name
    spider  = TaskSpider.load_tasks(name=name)
    if callback:
        subtask(callback).delay(spider)
    
@task
def period_fetch_task(spider):pass
    

    
        


