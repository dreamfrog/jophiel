import random
import warnings
from time import time
from collections import deque
from functools import partial
from .handlers import DownloadHandlers
from .middleware import DownloaderMiddlewareManager
from .. import conf

class Downloader(object):
    def __init__(self, settings):
        self.settings = settings
        self.slots = {}
        self.queue  = deque()
        self.handlers = DownloadHandlers()
        self.middlewares = DownloaderMiddlewareManager(*conf.DOWNLOAD_MIDDLEWARES)

    def fetch(self, request, spider):        
        return self.middlewares.download(self.handlers.download_request, request, spider)
    
