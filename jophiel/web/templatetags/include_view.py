'''
Created on 2012-2-26

@author: lzz
'''

from django import template
from django.conf import settings
import pystache
import os

register = template.Library()

template_dirs = getattr(settings, 'TEMPLATE_DIRS')
mustache_path = template_dirs

class IncludeViewNode(template.Node):
    def __init__(self, attr):
        self.attr = attr

    def render(self, context):
        view = context[self.attr] if self.attr in context else None
        if view:
            view.template_path = mustache_path
            return view.render()

def do_include_view(parser, token):
    """
    """
    bits = token.split_contents()
    if len(bits) not in  [2,3]:
        raise template.TemplateSyntaxError("%r tag takes two arguments: the location of the template file, and the template context" % bits[0])
    path = bits[1]
    attr = path[1:-1]
    return IncludeViewNode(attr)


register.tag("include_view", do_include_view)