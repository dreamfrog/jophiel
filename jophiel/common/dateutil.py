'''
Created on 2012-4-13

@author: lzz
'''

import time
import datetime

def get_as_date(value):
    """Return the key as a date value."""
    stamp = time.mktime(value)
    return datetime.datetime.fromtimestamp(stamp)

def now():
    return datetime.datetime.now()