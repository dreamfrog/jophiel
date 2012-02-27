from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'jophiel.views.home', name='home'),
    # url(r'^jophiel/', include('jophiel.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    
    # for development only  
    # This will only work if DEBUG is True.  
)

urlpatterns += staticfiles_urlpatterns()  

urlpatterns += patterns('',
        #('^names$', 'jophiel.views.index'),
        #('^names\/1$', 'jophiel.views.edit'),
        #('^templates\/index$', 'jophiel.views.index_template'),
        #('^templates\/edit$', 'jophiel.views.edit_template')
        )
    

urlpatterns += patterns('',
        ('^hello$', 'jophiel.views.index.hello'),
        #('^pystache$', 'jophiel.views.index.pystache'),
       )
