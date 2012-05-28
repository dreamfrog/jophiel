'''
Created on 2012-4-26

@author: lzz
'''

DEFAULT_RESPONSE_ENCODING = "utf-8"

SELECTORS_BACKEND = "lxml"

DOWNLOAD_MIDDLEWARES = {
    #'jophiel.crawler.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
    #'jophiel.crawler.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
    'jophiel.crawler.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
    'jophiel.crawler.downloadermiddleware.useragent.UserAgentMiddleware': 400,
    #'jophiel.crawler.downloadermiddleware.retry.RetryMiddleware': 500,
    'jophiel.crawler.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
    #'jophiel.crawler.downloadermiddleware.redirect.RedirectMiddleware': 600,
    #'jophiel.crawler.downloadermiddleware.cookies.CookiesMiddleware': 700,
    #'jophiel.crawler.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
    #'jophiel.crawler.downloadermiddleware.stats.DownloaderStats': 850,
    'jophiel.crawler.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
}

RESPONSE_CLASSES ={}
USER_AGENT = "jophiel"


# common file extensions that are not followed if they occur in links
IGNORED_EXTENSIONS = [
    # images
    'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
    'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

    # audio
    'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

    # video
    '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
    'm4a',

    # other
    'css', 'pdf', 'doc', 'exe', 'bin', 'rss', 'zip', 'rar',
]

DEFAULT_REQUEST_HEADERS = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en',
}

DOWNLOAD_TIMEOUT = 120

CACHE_TABLE_NAME = "webpage_cache"

HTTPCACHE_ENABLED = False
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_MISSING = False
HTTPCACHE_STORAGE = 'jophiel.crawler.downloadermiddleware.httpcache.FilesystemCacheStorage'
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_IGNORE_SCHEMES = ['file']
HTTPCACHE_DBM_MODULE = 'anydbm'