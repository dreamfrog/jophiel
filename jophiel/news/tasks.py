'''
Created on 2012-4-2

@author: lzz
'''

from celery.task import task
from .models import Feed
from .models import Planet

@task
def fetch_feed():pass

@task
def update_channels(planet_name):pass
    
@task
def update_channel(channel_name):
    channels = Feed.objects.filter(name = channel_name)
    for channel in channels:
        channel.update()
        