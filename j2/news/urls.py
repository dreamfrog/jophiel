'''
Created on 2012-4-11

@author: lzz
'''

from django.conf.urls.defaults import *

from django.conf.urls.defaults import *
from tastypie.api import Api


urlpatterns = patterns('news.views',
    url(r"^$",view = "index",name = "news_list"),
    url(r"^upload",view = "news_upload",name="news_upload")
)

