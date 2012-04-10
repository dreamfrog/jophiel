from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.template import RequestContext

from .constants import NEWS_KEY, NEWS_ARTICLE_PAGINATION
from .exceptions import NewsException
from .models import Article, Feed

import logging 

from mezzanine.utils import views

logger = logging.getLogger("jophiel.feeds")

def index(request):
    extra_context = {}
    sql = """select feeds_article.* from feeds_article
             where 1=1 and 
           """       
    if request.user.is_authenticated():
        sql = """select feeds_article.* from 
                     feeds_article ,feeds_feed,feeds_userfeeds 
                     where feeds_article.feed_id = feeds_feed.id and
                     """  
        sql += """feeds_feed.id = feeds_userfeeds.feed_id 
                and feeds_userfeeds.user_id = %s 
                and """ %request.user.id   
                
    if request.GET.get('feed_id',None):
        sql += " feeds_article.feed_id = %s and "%request.GET["feed_id"]
    sql +=" 1=1"
    
    qs  = Article.objects.raw(sql)
    page_num =request.GET.get('page', 1)
    extra_context["article_list"] = views.paginate(qs,page_num,5,8)
    querystring = request.GET.copy()
    if "page" in querystring:
        del querystring["page"]
    extra_context.update({'query': querystring.urlencode()})
    
    if request.user.is_authenticated():
        feeds = Feed.objects.filter(user=request.user,active = True).all()
    else:
        feeds = Feed.objects.filter(active = True).all()
    
    extra_context["feeds_list"] = feeds
    return views.render(request,"news/index.html",extra_context)

