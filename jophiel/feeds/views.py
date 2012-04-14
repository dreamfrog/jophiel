from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list
from django.template import RequestContext
from django.http import HttpResponseRedirect, Http404

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import ugettext as _

from .models import Article, Feed,UserFeeds
from .tasks import fetch_feed
from .forms import FeedAddForm
import logging 

from mezzanine.utils import views

logger = logging.getLogger("jophiel.feeds")


def default_article_sql(request):
    sql = """select feeds_article.* from feeds_article where 1=1 and 
           """        
    if request.GET.get('feed_id',None):
        sql += " feeds_article.feed_id = %s and "%request.GET["feed_id"]
    sql +=" 1=1"
    return sql

def user_article_sql(request):
    sql = """select feeds_article.* from feeds_article ,feeds_feed,feeds_userfeeds 
                 where feeds_article.feed_id = feeds_feed.id and
                 """  
    sql += """feeds_feed.id = feeds_userfeeds.feed_id  and feeds_userfeeds.user_id = %s 
            and """ %request.user.id  
            
    if request.GET.get('feed_id',None):
        sql += " feeds_article.feed_id = %s and "%request.GET["feed_id"]
    sql +=" 1=1"
    return sql  


def process_page(request,qs,page_num):
    qs = views.paginate(qs,page_num,5,8)
    return qs  
    
def process_articles(request,context):
    if request.user.is_authenticated():
        sql = user_article_sql(request)
    else:
        sql = default_article_sql(request)
    qs = Article.objects.raw(sql)  
    page_num =request.GET.get('page', 1)
    qs = process_page(request,qs,page_num)  
    context["article_list"] = qs
    
    querystring = request.GET.copy()
    if "page" in querystring:
        del querystring["page"]
    context.update({'article_query': querystring.urlencode()})   
     
    return qs

def process_feeds(request,context):
    if request.user.is_authenticated():
        feeds = Feed.objects.filter(user=request.user,active = True).all()
    else:
        feeds = Feed.objects.filter(active = True).all()
    
    context["feeds_list"] = feeds   
    querystring = request.GET.copy()
    if "feeds_page" in querystring:
        del querystring["feeds_page"] 
    if "page" in querystring:
        del querystring["page"]
        
    context.update({'feeds_query': querystring.urlencode()})   
    return feeds

def index(request):
    extra_context = {}
    articles = process_articles(request,extra_context)
    feeds =process_feeds(request,extra_context)   
    querystring = request.GET.copy()
    
    uploadform = FeedAddForm()
    extra_context.update({"feedupload_form":uploadform})
    return views.render(request,"feeds/index.html",extra_context)

@login_required
@require_POST
def upload_seed(request):
    form = FeedAddForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        seed_url = clean_data.get("feed_url","")
        if seed_url:
            try:
                obj = Feed.objects.get(url = seed_url)
            except Feed.DoesNotExist:
                obj = Feed(url = seed_url)
                obj.save()
            UserFeeds.objects.get_or_create(feed=obj,user=request.user)
            try:
                fetch_feed.delay(obj.id)
            except:
                pass
        return HttpResponseRedirect(reverse("feed_list"))
    else:
        messages.add_message(request, messages.ERROR, _('please input correct url '))
        return HttpResponseRedirect(reverse("feed_list"))