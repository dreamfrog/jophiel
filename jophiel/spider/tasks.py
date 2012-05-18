'''
Created on 2012-5-2

@author: lzz
'''
from celery.task import task
from celery.task import subtask
from celery.task.base import Task
from jophiel.crawler.http import Response
from jophiel.crawler.http import Request
from jophiel.crawler.download import Downloader
from jophiel.crawler.storage import WebPage
from jophiel.crawler.w3lib.http import headers_dict_to_raw,headers_raw_to_dict
from jophiel.crawler.http import Headers

from .tables import RequestTable
from .tables import RequestStat
from .storage import PageStorage

class DownloaderTask(Task):
    _downloader = None   
    abstract = True
    
    @property
    def downloader(self):
        if not self._downloader:
            self._downloader = Downloader()
        return self._downloader

    def after_return(self, *args, **kwargs):
        print("Task returned: %r" % (self.request, ))
    def on_success(self, retval, task_id, args, kwargs):pass    



@task(base=DownloaderTask,name="tasks.fetch_request",ignore_result=True)
def fetch_one_task(spider,request,callback=None):
    response = fetch_one_task.downloader.fetch(request,spider) 
    if isinstance(response,Response):
        RequestTable.storage_response(spider,request,response)
        PageStorage.storage_page(spider, request, response)
        if callback:
            subtask(callback).delay(spider,request,response)

@task(name="tasks.fetch_spiders",ignore_result=True)
def fetchs_task(spider,callback=None):
    table = RequestTable(spider.tablename)
    for request in table.iter_requests(RequestStat.STAT_NEED_DOWNLOAD):
        fetch_one_task.apply_async(args=(spider,request))
    
@task
def period_fetch_task(spider):pass
    
@task
def link_extract_task(spider): pass
        


