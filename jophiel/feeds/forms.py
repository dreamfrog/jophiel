'''
Created on 2012-4-10

@author: lzz
'''
from django import forms
from django.utils.translation import ugettext as _

class FeedAddForm(forms.Form):
    feed_url = forms.URLField(label=_('Feed Url'),widget=forms.TextInput(attrs={'size':'40'}))
