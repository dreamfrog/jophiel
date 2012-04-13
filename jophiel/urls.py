from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from django.conf import settings
from django.utils.translation import ugettext as _
from jophiel.utils.views import TV

LG = settings.LANGUAGE_CODE
from mezzanine.core.views import direct_to_template

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        url("^$", direct_to_template, {"template": "common/index.html"}, name="home"),
        ('^admin/',include(admin.site.urls)),   
        ('^feeds/',include("jophiel.feeds.urls")),
        ('^maps/',include("jophiel.maps.urls")),
        (r'^grappelli/', include('grappelli.urls')),  
        (r"^account/",include('account.urls')), 
        (r"^news/",include("jophiel.news.urls")),     
    )

urlpatterns += patterns("",
    (r'^$', TV("help/%s/index.html" % LG), {}, 'help-index'),
    (r'^%s/$' % _('about'), TV("help/%s/about.html" % LG), {}, 'help-about'),
    (r'^%s/$' % _('terms'), TV("help/%s/terms.html" % LG), {}, 'help-terms'),
    (r'^%s/$' % _('privacy'), TV("help/%s/privacy.html" % LG), {}, 'help-privacy'),
    (r'^%s/$' % _('making-requests'), TV("help/%s/making-requests.html" % LG), {}, 'help-making_requests'),
    (r'^%s/$' % _('your-privacy'), TV("help/%s/your-privacy.html" % LG), {}, 'help-your_privacy'),
    (r'^%s/$' % _('for-foi-officers'), TV("help/%s/foi-officers.html" % LG), {}, 'help-foi_officers'),
)

urlpatterns += patterns('',
        ("^", include("mezzanine.urls")),                        
    )

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler500 = "mezzanine.core.views.server_error"
