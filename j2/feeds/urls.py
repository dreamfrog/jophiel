from django.conf.urls.defaults import *

from django.conf.urls.defaults import *
from tastypie.api import Api
from .api import ArticleResource,UserResource
from . import views
v1_api = Api(api_name='v1')
#v1_api.register(UserResource())
v1_api.register(ArticleResource())

urlpatterns = patterns('',
    url(r"^$",view = views.index,name = "feed_list"),
    url(r"^upload",view = views.upload_seed,name="feed_upload")
)

"""api"""
urlpatterns += patterns('',
    # The normal jazz here then...
    (r'^api/', include(v1_api.urls)),
)
