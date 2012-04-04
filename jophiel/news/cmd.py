'''
Created on 2012-4-4

@author: lzz
'''
from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from .constants import NEWS_KEY, NEWS_ARTICLE_PAGINATION
from .exceptions import NewsException
from .models import Article, Feed

def run_download(request, *args, **kwargs):
    if request.GET.get('key') == NEWS_KEY:
        articles = 0
        for feed in Feed.objects.filter(active=True):
            try:
                result = feed.process_feed()
            except NewsException:
                pass
            else:
                articles += feed.new_articles_added
        Article.objects.expire_articles()
        return HttpResponse('Done: %d' % (articles))
    return HttpResponse('')