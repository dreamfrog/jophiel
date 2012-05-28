'''
Created on 2012-4-2

@author: lzz
'''

from __future__ import absolute_import

from celery.bin.celeryctl import celeryctl, Command as _Command

from djcelery import __version__
from djcelery.app import app
from djcelery.management.base import CeleryCommand

# Django hijacks the version output and prints its version before our
# version. So display the names of the products so the output is sensible.
_Command.version = "celery %s\ndjango-celery %s" % (_Command.version,
                                                    __version__)

from jophiel.spiders import crawl

class Command(CeleryCommand):
    """Run the celery control utility."""
    help = "celery control utility"

    def run_from_argv(self, argv):
        crawl.start_crawl("dianping")
        