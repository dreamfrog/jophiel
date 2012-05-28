import random
import warnings
from time import time
from collections import deque
from functools import partial
from .handlers import DownloadHandlers
from .middleware import DownloaderMiddlewareManager
from jophiel.crawler import conf

class Downloader(object):
    def __init__(self):
        self.slots = {}
        self.queue  = deque()
        self.handlers = DownloadHandlers()
        self.middlewares = DownloaderMiddlewareManager()

    def fetch(self, request, spider):        
        return self.middlewares.download(self.handlers.download_request, request, spider)
    
