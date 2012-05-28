from __future__ import absolute_import

from urlparse import urlsplit
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

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

urlpatterns += patterns("",
                        url(r"^account/",include('account.urls')), 
                        url(r'^crawl/',include("spider.urls")),
                        url(r'^schedules/',include("schedule.urls")),
                        )