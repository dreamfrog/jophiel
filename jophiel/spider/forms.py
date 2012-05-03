'''
Created on 2012-5-2

@author: lzz
'''

from django import forms
from django.utils.translation import ugettext as _

from jophiel.jsonfield import JSONFormField

class SpiderForm(forms.Form):
    name  = forms.CharField(label = _("Spider Name"))
    params = JSONFormField( label = _("Spider Params"),
                              help_text = _("input json parameters"),
                              widget=forms.Textarea())
    