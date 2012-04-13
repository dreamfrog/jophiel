# Create your views here.

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
from mezzanine.utils import views

import logging 
logger = logging.getLogger("jophiel.news")
from .models import ExtractResults,UrlSeeds
from .forms import FeedAddForm 
from .tasks import url_extract_task

def index(request):
    context = {}
    lists = ExtractResults.objects.all()
    context["news_list"] = lists
    context["feedupload_form"] = FeedAddForm()
    return views.render(request,"news/index.html",context)    

@login_required
@require_POST
def news_upload(request):
    form = FeedAddForm(request.POST)
    if form.is_valid():
        clean_data = form.cleaned_data
        seed_url = clean_data.get("feed_url","")
        if seed_url:
            UrlSeeds.objects.get_or_create(url = seed_url)
            try:
                url_extract_task.delay(seed_url)
            except:
                pass
        return HttpResponseRedirect(reverse("news_list"))
    else:
        messages.add_message(request, messages.ERROR, _('please input correct url '))
        return HttpResponseRedirect(reverse("news_list"))