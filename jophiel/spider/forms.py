'''
Created on 2012-5-2

@author: lzz
'''

from django import forms
from django.utils.translation import ugettext as _

from jophiel.jsonfield import JSONFormField
from .models import Spider

class SpiderForm(forms.ModelForm):
    name  = forms.CharField(label = _("Spider Name"))
    description = forms.CharField(label = _("Description"),
                                  widget = forms.Textarea(),
                                  initial = "spider infomation"
                                  )
    params = JSONFormField( label = _("Spider Params"),
                              help_text = _("input json parameters"),
                              widget=forms.Textarea(),
                              initial = "{}"
                              ) 
    domains = JSONFormField(label = _("Domains"),
                              help_text = _("allowed domains"),
                              widget = forms.Textarea(),
                              initial = "[]"
                            )
    
    urls = JSONFormField(label = _("Start Urls"),
                            widget = forms.Textarea(),
                            initial = "[]"
                            )
    rules = JSONFormField(label = _("Extract Links Rules"),
                          widget = forms.Textarea(),
                          initial = "[]"
                          )
    
    class Meta:
        model = Spider