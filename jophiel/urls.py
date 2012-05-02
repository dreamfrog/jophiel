from __future__ import absolute_import

from urlparse import urlsplit
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from . import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        ('^admin/',include(admin.site.urls)),   
    )

# Grappelli admin skin.
_pattern = urlsplit(settings.ADMIN_MEDIA_PREFIX).path.strip("/").split("/")[0]
if getattr(settings, "PACKAGE_NAME_GRAPPELLI") in settings.INSTALLED_APPS:
    urlpatterns += patterns("",
        ("^grappelli/", include("%s.urls" % settings.PACKAGE_NAME_GRAPPELLI)),
    )


task_pattern = r'(?P<task_id>[\w\d\-\.]+)'

urlpatterns += patterns("",
    url(r'^%s/done/?$' % task_pattern, views.is_task_successful,
        name="celery-is_task_successful"),
    url(r'^%s/status/?$' % task_pattern, views.task_status,
        name="celery-task_status"),
    url(r'^tasks/?$', views.registered_tasks, name='celery-tasks'),
)
