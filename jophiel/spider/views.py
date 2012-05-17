'''
Created on 2012-5-2

@author: lzz
'''
from django.http import HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse
from django.views.decorators.http import require_POST
from .forms import SpiderForm
from .utils import create_seed_request

def render(request, templates, dictionary=None,
           context_instance=None,**kwargs):
    dictionary = dictionary or {}
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = RequestContext(request, dictionary)
    return TemplateResponse(request, templates, context_instance, **kwargs)

def list(request):pass

def index(request):
    context = {}
    context["form"] = SpiderForm()
    return render(request,"spiders/create_spider.html",context)

def detail(request):pass

@require_POST
def create(request):
    form = SpiderForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        spider = form.save()
        create_seed_request(spider,clean_data.get("urls",""))
        
        
    
