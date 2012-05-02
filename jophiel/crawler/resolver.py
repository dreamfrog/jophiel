'''
Created on 2012-4-26

@author: lzz
'''
import socket

from .utils.datatypes import LocalCache

# TODO: cache misses
# TODO: make cache size a setting

dnscache = LocalCache(10000)