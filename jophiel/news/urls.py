from django.conf.urls.defaults import *

urlpatterns = patterns('jophiel.news.views',
    url(r'^(?P<url_path>[/\w-]*)',
        view='article_list',
        name='news_article_index'
    )
)
