'''
Created on 2012-4-14

@author: lzz
'''
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, ugettext_lazy

from j2.plugins.base import BaseBlock
from j2 import plugins

from .models import Spider

class SpiderListBlock(BaseBlock):
    name = 'SpiderListBlock'
    default_place = 'meta'
    fixed_place = True
    is_addable = False
    help_text = ugettext_lazy('Block represents global spider lists')
    verbose_name = ugettext_lazy('spider List block')
    render_template = "spiders/list_spider.html"
    
    def render(self, request, place, context, *args, **kwargs):
        spider_list = Spider.objects.all()       
        return self.render_block(
            request, template_name=self.render_template,
            context={ 'spider_list': spider_list})

plugins.register(SpiderListBlock)
