from django.conf.urls.defaults import patterns, include, url

from django.contrib.admin.sites import NotRegistered
from django.http import HttpResponse
from django.utils.translation import ugettext as _
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
        url("^$", direct_to_template, {"template": "common/index.html"}, name="home"),
        ('^feeds/',include("feeds.urls")),
        ('^maps/',include("maps.urls")),
        (r"^account/",include('account.urls')), 
        (r"^news/",include("news.urls")),     
    )


# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler500 = "jophiel.core.views.server_error"
