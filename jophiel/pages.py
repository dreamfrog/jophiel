'''
Created on 2012-4-23

@author: lzz
'''
from collections import defaultdict
from django.conf import settings

"""
    page={
        "name":"show_name",
        "url": "page_url",
        "description",
    }

"""

pages = []
LOADED = False

def autodiscover():
    """ 
    Taken from ``django.contrib.admin.autodiscover`` and used to run
    any calls to the ``processor_for`` decorator.
    """
    global LOADED
    if LOADED:
        return
    LOADED = True
    
    for app in settings.INSTALLED_APPS:
        try:
            module = __import__("%s.modules" % app)
            if "name" in module.page and "url" in module.page:
                pages.append(module.page)
        except ImportError:
            pass