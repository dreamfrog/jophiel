'''
Created on 2012-4-2

@author: lzz
'''

from celery.task import task
from celery.task.sets import TaskSet

from .models import Feed

@task(ignore_result=True, serializer="pickle", compression="zlib")
def fetch_feed(feed_id):
    try:
        feed = Feed.objects.get(id = feed_id)
        feed.process_feed()
    except:
        pass

        
@task(ignore_result=True, serializer="pickle", compression="zlib")   
def run_download():
    tasks = []
    for feed in Feed.objects.filter(active=True).order_by('-updated'):
        subtask = fetch_feed.subtask(feed.id)
        tasks.append(subtask)
        
    subtasks = TaskSet(tasks)
    subtasks.apply_async()
    