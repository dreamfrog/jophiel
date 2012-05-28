from django.http import HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.utils.translation import ugettext as _
from mezzanine.utils import views

from .models import Feed,UserFeeds
from .tasks import fetch_feed
from .forms import FeedAddForm

import logging 
logger = logging.getLogger("jophiel.feeds")
    
def index(request):
    extra_context = {}
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