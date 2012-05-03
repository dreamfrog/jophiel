'''
Created on 2012-5-2

@author: lzz
'''
from django.http import HttpResponse
from django.template import RequestContext
from django.template.response import TemplateResponse

from .forms import SpiderForm

def render(request, templates, dictionary=None, context_instance=None,
           **kwargs):
    dictionary = dictionary or {}
    if context_instance:
        context_instance.update(dictionary)
    else:
        context_instance = RequestContext(request, dictionary)
    return TemplateResponse(request, templates, context_instance, **kwargs)

def list(request):pass

def index(request):
    context = {}
    print "hello"
    context["form"] = SpiderForm()
    return render(request,"jophiel/base.html",context)

def detail(request):pass

def create(request):
    request.GET
