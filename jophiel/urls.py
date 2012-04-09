from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

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
    )

from django.conf import settings
from django.utils.translation import ugettext as _
from django.views.generic import TemplateView

LG = settings.LANGUAGE_CODE

def TV(template):
    return TemplateView.as_view(template_name=template)

urlpatterns += patterns("",
    (r'^$', TV("help/%s/index.html" % LG), {}, 'help-index'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('about'), TV("help/%s/about.html" % LG), {}, 'help-about'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('terms'), TV("help/%s/terms.html" % LG), {}, 'help-terms'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('privacy'), TV("help/%s/privacy.html" % LG), {}, 'help-privacy'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('making-requests'), TV("help/%s/making-requests.html" % LG), {}, 'help-making_requests'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('your-privacy'), TV("help/%s/your-privacy.html" % LG), {}, 'help-your_privacy'),
    # Translators: URL part of /help/
    (r'^%s/$' % _('for-foi-officers'), TV("help/%s/foi-officers.html" % LG), {}, 'help-foi_officers'),


)

urlpatterns += patterns('',
        ("^", include("mezzanine.urls")),                        
    )

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler500 = "mezzanine.core.views.server_error"
