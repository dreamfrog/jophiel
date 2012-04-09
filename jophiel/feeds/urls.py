from django.conf.urls.defaults import *

from django.conf.urls.defaults import *
from tastypie.api import Api

from .api import ArticleResource,UserResource

v1_api = Api(api_name='v1')
#v1_api.register(UserResource())
v1_api.register(ArticleResource())

urlpatterns = patterns('feeds.views',
    url(r"^$",view = "index",name = "feed_list"),
    #url(r"^list",view = "article_list",name="articles")
)

"""api"""
urlpatterns += patterns('',
    # The normal jazz here then...
    (r'^api/', include(v1_api.urls)),
)