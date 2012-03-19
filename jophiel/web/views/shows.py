
from django import http
import pystache
from jophiel import settings
 
pystache.View.template_path = settings.MEDIA_ROOT

