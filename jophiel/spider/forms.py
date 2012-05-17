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
                                  widget = forms.Textarea()
                                  )
    params = JSONFormField( label = _("Spider Params"),
                              help_text = _("input json parameters"),
                              widget=forms.Textarea())
    urls = forms.CharField(label = _("Start Urls"),
                            widget = forms.Textarea())
    
    class Meta:
        model = Spider