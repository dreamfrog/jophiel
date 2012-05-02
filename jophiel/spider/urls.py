'''
Created on 2012-5-2

@author: lzz
'''

from urlparse import urlsplit
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from . import views

urlpatterns = patterns('',
        ('^$',views.list), 
        ('^detail/',views.detail),
    )