'''
Created on 2012-4-1

@author: lzz
'''

from celery.task import task
from eventlet.green import urllib2

from celery.task import task
from .crawl import start_crawl

from multiprocessing import Process
import signal

@task
def crawl_web(task_name):
    start_crawl(task_name)

@task
def urlopen(url):
    print("Opening: %r" % (url, ))
    try:
        body = urllib2.urlopen(url).read()
    except Exception, exc:
        print("URL %r gave error: %r" % (url, exc))
    return len(body)