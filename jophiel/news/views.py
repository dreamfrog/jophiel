from django.conf import settings
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views.generic.list_detail import object_list

from .constants import NEWS_KEY, NEWS_ARTICLE_PAGINATION
from .exceptions import NewsException
from .models import Article, Feed


def article_list(request, url_path='', template_name='news/article_list.html'): 
    extra_context = {}
    qs = Article.objects.filter(isexpired=False)
    
    if request.GET.get('q', None):
        qs = qs.filter(title__icontains=request.GET['q'])
        extra_context.update({'search_query': request.GET['q']})

    try:
        page = int(request.GET.get('page', 0))
    except ValueError:
        raise Http404
        
    return object_list(
        request,
        queryset=qs,
        template_object_name='article',
        extra_context=extra_context,
        paginate_by=NEWS_ARTICLE_PAGINATION,
        page=page
    )
