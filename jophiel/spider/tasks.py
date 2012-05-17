'''
Created on 2012-5-2

@author: lzz
'''
from celery.task import task
from celery.task.base import Task
from jophiel.crawler.download import Downloader

class DownloaderTask(Task):
    _downloader = None   
    abstract = True
    
    @property
    def downloader(self):
        if not self._downloader:
            self._downloader = Downloader()
        return self._downloader
            

@task(base=DownloaderTask)
def fetch_task(request,spider):
    response = fetch_task.downloader.fetch(request,spider) 
    return response
    
@task
def period_fetch_task(spider):pass
    
@task
def link_extract_task(spider): pass
        


