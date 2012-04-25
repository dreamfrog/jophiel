from django.conf.urls.defaults import patterns, include, url
from urlparse import urlsplit

from django.contrib.admin.sites import NotRegistered
from django.http import HttpResponse

from django.utils.translation import ugettext as _
from jophiel.utils.views import TV

from jophiel.core.views import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url("^$", direct_to_template, {"template": "common/index.html"}, name="home"),
        ('^admin/',include(admin.site.urls)),   
        #(r"^account/",include('account.urls')), 
    )

from jophiel.conf import settings

# Return a robots.txt that disallows all spiders when DEBUG is True.
if getattr(settings, "DEBUG", False):
    urlpatterns += patterns("",
        ("^robots.txt$", lambda r: HttpResponse("User-agent: *\nDisallow: /",
                                                mimetype="text/plain")),
    )

# Grappelli admin skin.
_pattern = urlsplit(settings.ADMIN_MEDIA_PREFIX).path.strip("/").split("/")[0]
if getattr(settings, "PACKAGE_NAME_GRAPPELLI") in settings.INSTALLED_APPS:
    urlpatterns += patterns("",
        ("^grappelli/", include("%s.urls" % settings.PACKAGE_NAME_GRAPPELLI)),
    )

# Miscellanous Mezzanine patterns.
urlpatterns += patterns("",
    ("^", include("jophiel.core.urls")),
    ("^", include("jophiel.generic.urls")),
)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler500 = "jophiel.core.views.server_error"
