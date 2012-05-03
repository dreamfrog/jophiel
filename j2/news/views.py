# Create your views here.

from django.http import HttpResponseRedirect

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

from .models import UrlSeeds

def process_page(request,qs,page_num):
    qs = views.paginate(qs,page_num,5,8)
    return qs  

def index(request):
    context = {}
    lists = ExtractResults.objects.all()
    page_num = request.GET.get("page",1)
    qs = process_page(request,lists,page_num)
    context["news_list"] = qs
    context["feedupload_form"] = FeedAddForm()
    seeds = UrlSeeds.objects.all()
    context["feeds_list"] = qs    
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