from django.conf.urls.defaults import *
import os

urlpatterns = patterns('jophiel.maps',
    (r'^$', 'mapview.index'),

    (r'^/$', 'mapview.index'),
    (r'^map$', 'mapview.map'),
    (r'^detail$', 'mapview.detail'),
    (r'^main$', 'mapview.main'),
    
    (r'^list$', 'mapview.list'),
    (r'^city$', 'mapview.cityinfo'),
	
)
