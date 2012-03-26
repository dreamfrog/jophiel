"""
Scrapy - a screen scraping framework written in Python
"""

version_info = (0, 15, 1)
__version__ = "0.15.1"

import sys, os, warnings

if sys.version_info < (2, 5):
    print "Scrapy %s requires Python 2.5 or above" % __version__
    sys.exit(1)

# ignore noisy twisted deprecation warnings
warnings.filterwarnings('ignore', category=DeprecationWarning, module='twisted')

# monkey patches to fix external library issues
from scrapy.xlib import twisted_250_monkeypatches, urlparse_monkeypatches

# optional_features is a set containing Scrapy optional features
optional_features = set()

try:
    import OpenSSL
except ImportError:
    pass
else:
    optional_features.add('ssl')

try:
    import boto
except ImportError:
    pass
else:
    optional_features.add('boto')

settings = {
        "LOG_ENABLED": True,
        "LOG_ENCODING": 'utf-8',
        "LOG_FORMATTER": 'scrapy.logformatter.LogFormatter',
        "LOG_STDOUT": False,
        "LOG_LEVEL": 'DEBUG',
        "LOG_FILE": None,
        
        "STATS_ENABLED":True,
        "STATS_CLASS":"scrapy.statscol.MemoryStatsCollector",
        "STATS_DUMP" : True,
        
        "TRACK_REFS" :True,
        "ENCODING_ALIASES" : {},
        "ENCODING_ALIASES_BASE" :{
            # gb2312 is superseded by gb18030
            'gb2312': 'gb18030',
            'chinese': 'gb18030',
            'csiso58gb231280': 'gb18030',
            'euc- cn': 'gb18030',
            'euccn': 'gb18030',
            'eucgb2312-cn': 'gb18030',
            'gb2312-1980': 'gb18030',
            'gb2312-80': 'gb18030',
            'iso- ir-58': 'gb18030',
            # gbk is superseded by gb18030
            'gbk': 'gb18030',
            '936': 'gb18030',
            'cp936': 'gb18030',
            'ms936': 'gb18030',
            # latin_1 is a subset of cp1252
            'latin_1': 'cp1252',
            'iso-8859-1': 'cp1252',
            'iso8859-1': 'cp1252',
            '8859': 'cp1252',
            'cp819': 'cp1252',
            'latin': 'cp1252',
            'latin1': 'cp1252',
            'l1': 'cp1252',
            # others
            'zh-cn': 'gb18030',
            'win-1251': 'cp1251',
            'macintosh' : 'mac_roman',
            'x-sjis': 'shift_jis',
        },
        "DEFAULT_RESPONSE_ENCODING" : 'ascii',
        
        "DOWNLOAD_HANDLERS" : {},
        "DOWNLOAD_HANDLERS_BASE" : {
            'file': 'scrapy.core.downloader.handlers.file.FileDownloadHandler',
            'http': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
            'https': 'scrapy.core.downloader.handlers.http.HttpDownloadHandler',
        },
        
        "CRAWLSPIDER_FOLLOW_LINKS":True,
        "SELECTORS_BACKEND":"lxml",
        
        "CLOSESPIDER_TIMEOUT" : 1,
        "CLOSESPIDER_PAGECOUNT": 1,
        "CLOSESPIDER_ITEMCOUNT": 1,
        "CLOSESPIDER_PAGECOUNT": 1,
        "CLOSESPIDER_ERRORCOUNT":1,
        "DOWNLOADER_HTTPCLIENTFACTORY":'scrapy.core.downloader.webclient.ScrapyHTTPClientFactory',
        "DOWNLOADER_CLIENTCONTEXTFACTORY":'scrapy.core.downloader.webclient.ScrapyClientContextFactory',
        "RESPONSE_CLASSES":{}
    }
