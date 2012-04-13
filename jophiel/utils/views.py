'''
Created on 2012-4-10

@author: lzz
'''
from django.views.generic import TemplateView

def TV(template):
    return TemplateView.as_view(template_name=template)