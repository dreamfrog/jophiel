'''
Created on 2012-5-2

@author: lzz
'''
from django.http import HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from .paginator import Paginator, EmptyPage, PageNotAnInteger,paginate

from .forms import SpiderForm
from .utils import create_seed_request,create_spider_task
from .models import Spider
from .tables import RequestTable

def render(request, templates, dictionary=None,
           context_instance=None,**kwargs):
    dictionary = dictionary or {}
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = RequestContext(request, dictionary)
    return TemplateResponse(request, templates, context_instance, **kwargs)

def spiders(request):
    return render(request,"spiders/spiders.html")

def urls(request):
    id = request.GET["id"]
    spider = Spider.objects.get(id = id)
    table = RequestTable(str(spider.tablename))
    count  = table.count_items()
    page = request.GET.get('page',1)
    
    pages = paginate(count,page,20,10)
    limit=pages.end_index()-pages.start_index()
    items = table.iter_items(offset=pages.start_index(),limit=limit)
    context = {
               "urls":items,
               'pages':pages,
               'spider':spider
               }
    return render(request,"spiders/urls.html",context)

def index(request):
    context = {}
    context["form"] = SpiderForm()
    return render(request,"spiders/create_spider.html",context)

def create_spider(request):
    context = {}
    context["form"] = SpiderForm()
    return render(request,"spiders/create_spider.html",context)

@require_POST
def create_spider_upload(request):
    form = SpiderForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        spider = form.save()
        create_seed_request(spider,clean_data.get("urls",""))
        create_spider_task(spider)
        return redirect(reverse("spider_list"))
    context = {}
    context["form"] = form
    return render(request,"spiders/create_spider.html",context)
        
        
    
