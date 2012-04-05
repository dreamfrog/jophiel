from django.conf.urls.defaults import *
import os
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

BASE_ROOT = os.path.abspath(os.path.split(__file__)[0])
#print BASE_ROOT
TEMPLATE_ROOT = BASE_ROOT + '/template'
JS_ROOT = BASE_ROOT + '/js'
MAP_ROOT = BASE_ROOT + '/images'
RES_ROOT = BASE_ROOT + '/res'
CSSIMAGE_ROOT = BASE_ROOT + '/css/ui-lightness/images'
CSS_ROOT = BASE_ROOT + '/css'

LIB_ROOT = BASE_ROOT + '/lib'
THEME_ROOT = BASE_ROOT + '/theme'
IMG_ROOT = BASE_ROOT + '/img'

MEDIA_ROOT= BASE_ROOT + '/media'
print MEDIA_ROOT
urlpatterns = patterns('',
    (r'^$', 'map.mapview.index'),

    (r'^/$', 'map.mapview.index'),
    (r'^map$', 'map.mapview.map'),
    (r'^save_text/.*', 'app.views.save_text'),
    (r'^get_text/.*', 'app.views.get_text'),
    (r'^detail$', 'map.mapview.detail'),
    (r'^main$', 'map.mapview.main'),
    
    (r'^list$', 'map.mapview.list'),
    (r'^city$', 'map.mapview.cityinfo'),
	
    # static direcory
    (r'^map_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': MEDIA_ROOT, 'show_indexes': True}),
              
    # Example:
    # (r'^JAM/', include('JAM.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     #(r'^admin/', include(admin.site.urls)),
)
