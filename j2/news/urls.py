'''
Created on 2012-4-11

@author: lzz
'''

from django.conf.urls.defaults import *

from django.conf.urls.defaults import *
from tastypie.api import Api
from . import views 

urlpatterns = patterns('',
    url(r"^$",view = views.index,name = "news_list"),
    url(r"^upload",view = views.news_upload,name="news_upload")
)

