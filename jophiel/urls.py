from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
        ('^admin/',include(admin.site.urls)),   
        ('^news/',include("jophiel.news.urls"))            
    )
urlpatterns += patterns('',
        (r'^grappelli/', include('grappelli.urls')),
)
