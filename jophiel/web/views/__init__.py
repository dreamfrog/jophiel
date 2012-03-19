import math, random
from django.http import HttpResponse
from jophiel import settings
from jinja2 import FileSystemLoader, Environment

template_dirs = getattr(settings, 'TEMPLATE_DIRS')
default_mimetype = getattr(settings, 'DEFAULT_CONTENT_TYPE')
env = Environment(loader=FileSystemLoader(template_dirs))

def render_to_response(filename, context={}, mimetype=default_mimetype):
    template = env.get_template(filename)
    rendered = template.render(**context)
    return HttpResponse(rendered, mimetype=mimetype)


import os
import pystache

class BasicPystache(pystache.View):
    template_path = os.path.join(os.path.dirname(settings.__file__), 'templates/mustache')
    def __init__(self, template=None, context=None, **kwargs):
        super(BasicPystache, self).__init__(template=None, context=None, **kwargs)
