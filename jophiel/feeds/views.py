from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.template import RequestContext

from .constants import NEWS_KEY, NEWS_ARTICLE_PAGINATION
from .exceptions import NewsException
from .models import Article, Feed

from django.shortcuts import render_to_response
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging 

from mezzanine.utils import views

logger = logging.getLogger("jophiel.feeds")


def index(request):
    extra_context = {}
    qs = Article.objects.filter(isexpired=False)
    if request.GET.get('q', None):
        qs = qs.filter(title__icontains=request.GET['q'])
    if request.GET.get('feed_id',None):
        qs  = qs.filter(feed=request.GET["feed_id"])
    qs  = qs.all()
    
    querystring = request.GET.copy()
    if "page" in querystring:
        del querystring["page"]
    querystring = querystring.urlencode()
    extra_context.update({'search_query': querystring})
    
    page_num =request.GET.get('page', 1)
    lists = views.paginate(qs,page_num,5,8)
    extra_context["article_list"] = lists
        
    feeds = Feed.objects.filter(active = True).all()
    extra_context["feeds_list"] = feeds
    return views.render(request,"news/index.html",extra_context)

