'''
Created on 2012-4-14

@author: lzz
'''
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, ugettext_lazy

from jophiel.plugins.base import BaseBlock
from jophiel import plugins

from .models import Feed
from .forms import FeedAddForm
from .utils import fetch_user_article,fetch_default_article,process_page

class FeedsListBlock(BaseBlock):
    name = 'FeesListBlock'
    default_place = 'meta'
    fixed_place = True
    is_addable = False
    help_text = ugettext_lazy('Block represents global feed lists')
    verbose_name = ugettext_lazy('feed List block')
    render_template = "feeds/feeds_list.html"
    
    def render(self, request, place, context, *args, **kwargs):
        
        if request.user.is_authenticated():
            feeds_list = Feed.objects.filter(user=request.user,active = True).all()
        else:
            feeds_list = Feed.objects.filter(active = True).all()       
        querystring = request.GET.copy()
        if "feeds_page" in querystring:
            del querystring["feeds_page"] 
        feed_url = querystring.urlencode()  
        return self.render_block(
            request, template_name=self.render_template,
            context={'feeds_url': feed_url,
                     'feeds_list': feeds_list})

class FeedsUploadBlock(BaseBlock):
    name = 'FeedsUploadBlock'
    default_place = 'meta'
    fixed_place = True
    is_addable = False
    help_text = ugettext_lazy('Block represents global feed lists')
    verbose_name = ugettext_lazy('feed List block')
    render_template = "feeds/feeds_upload.html"
    
    def render(self, request, place, context, *args, **kwargs):
        return self.render_block(
            request, template_name=self.render_template,
            context={"feedupload_form":FeedAddForm()})

class ArticleListBlock(BaseBlock):
    name = 'ArticleListBlock'
    default_place = 'meta'
    fixed_place = True
    is_addable = False
    help_text = ugettext_lazy('Block represents Article lists')
    verbose_name = ugettext_lazy('feed List block')
    render_template = "feeds/articles_list.html"
    
    def render(self, request, place, context, *args, **kwargs):
        feed_id = request.GET.get('feed_id',None)    
        if request.user.is_authenticated():
            qs = fetch_user_article(request.user,feed_id)
        else:
            qs = fetch_default_article(feed_id)
            
        page_num =request.GET.get('page', 1)
        qs = process_page(request,qs,page_num)  
        context["article_list"] = qs
        
        querystring = request.GET.copy()
        if "page" in querystring:
            del querystring["page"]
            
        return self.render_block(
            request, template_name=self.render_template,
            context={"article_list":qs,
                     "article_query":querystring.urlencode()
                     })    
        
plugins.register(FeedsListBlock)
plugins.register(FeedsUploadBlock)
plugins.register(ArticleListBlock)