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

class Command(BaseCommand):
    args = '<feed_name feed_url>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        if len(args)<1:
            exit()
        feed_url = args[0]
        feed_name = ""
        if len(args) >1:
            feed_name = args[1]
        try:
            feed = Feed.objects.get(url = feed_url)
        except:
            feed = Feed(name = feed_name,url = feed_url)
        
        feed.process_feed()
