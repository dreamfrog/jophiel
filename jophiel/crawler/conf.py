'''
Created on 2012-4-26

@author: lzz
'''
from .downloadermiddleware import *

DEFAULT_RESPONSE_ENCODING = "utf-8"

SELECTORS_BACKEND = "lxml"

DOWNLOAD_MIDDLEWARES = [
                        
]

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