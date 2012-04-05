from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'app.views.index'),
    (r'^map/.*', 'app.mapview.index'),    
    (r'^save_text/.*','app.views.save_text'),
    (r'^get_text/.*','app.views.get_text'),

    # static direcory
    (r'(^|/)js/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'html', 'show_indexes': True}),
    
    # Example:
    # (r'^JAM/', include('JAM.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)
