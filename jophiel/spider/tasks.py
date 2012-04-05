'''
Created on 2012-4-1

@author: lzz
'''

from celery.task import task
from .crawl import start_crawl

from multiprocessing import Process
import signal

@task
def crawl_web(task_name):
    start_crawl(task_name)
