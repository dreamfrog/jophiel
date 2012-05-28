'''
Created on 2012-4-6

@author: lzz
'''
import datetime
import logging
import os
import time
from optparse import make_option
from django.conf import settings
from django.core.management.base import NoArgsCommand
from django.db.models import Q

from jophiel.feeds.exceptions import NewsException
from jophiel.feeds.models import Feed, FeedMeta,Article

from django.core.management.base import BaseCommand, CommandError
from jophiel.feeds.utils import fetch_feed

class Command(BaseCommand):
    args = '<feed_name feed_url>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if len(args)<1:
            exit()
        file_name = args[0]
        file = open(file_name,"r")
        with open(file_name,"r") as file:
            for line in file:
                values = line.split()
                print "--processing:",values
                feed_name = ""
                if len(args)>2:
                    feed_name,feed_url = values[0],values[1]
                else:
                    feed_url = values[0]
        
                try:
                    feed = Feed.objects.get(url = feed_url)
                except:
                    feed = Feed(name = feed_name,url = feed_url)
        
                data = fetch_feed(feed.url)
                feed.process_feed(data)
