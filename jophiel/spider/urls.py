'''
Created on 2012-5-2

@author: lzz
'''

from urlparse import urlsplit
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from . import views

urlpatterns = patterns('',
        url('^$',views.index,name = "list_spider"), 
        url('^detail/',views.detail, name = "detail_spider"),
        url('^create/',views.create, name = "create_spider"),
    )