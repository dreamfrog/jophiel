'''
Created on 2012-5-2

@author: lzz
'''

from urlparse import urlsplit
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from . import views

urlpatterns = patterns('',
        url('^$',views.spiders,name = "spider_list"), 
        #url('^detail/',views.detail, name = "spider_detail"),
        url('^create/',views.create_spider, name = "spider_create"),
        url('^spider_upload/',views.create_spider_upload, name="spider_create_upload"),
        url('^urls/',views.urls,name="spider_urls_list"),
    )