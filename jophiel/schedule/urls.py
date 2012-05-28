'''
Created on 2012-5-28

@author: lzz
'''

from __future__ import absolute_import

from urlparse import urlsplit
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from . import views

task_pattern = r'(?P<task_id>[\w\d\-\.]+)'

urlpatterns = patterns("",
    url(r'^%s/done/?$' % task_pattern, views.is_task_successful,
        name="celery-is_task_successful"),
    url(r'^%s/status/?$' % task_pattern, views.task_status,
        name="celery-task_status"),
    url(r'^tasks/?$', views.registered_tasks, name='celery-tasks'),
)
