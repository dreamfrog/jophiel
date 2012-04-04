#coding=utf-8
from django import forms
import settings
class BaseForm(forms.Form): 
    enginechoose = forms.MultipleChoiceField(choices=(
                              ("mpoi", "mpoi"),
                              ("web", "web"),
                             ), initial=["mpoi"], widget=forms.CheckboxSelectMultiple(), required=False)  
    def __init__(self, *callback_args, **callback_kwargs):
        forms.Form.__init__(self, *callback_args, **callback_kwargs)

class SearchForm(BaseForm):
    cityname = forms.CharField()
    kw = forms.CharField()
    page = forms.CharField(initial="1", required=False)
    searchtype = forms.CharField(initial="region", required=False)
    lat = forms.CharField(required=False)
    lng = forms.CharField(required=False)
    distance = forms.CharField(required=False)
    
    def __init__(self, *callback_args, **callback_kwargs):
        BaseForm.__init__(self, *callback_args, **callback_kwargs)

    #map=forms.CharField()
    #p=forms.CharField()
    
    #urlencode_kw=forms.CharField()
class DetailForm(BaseForm):
    cityname = forms.CharField()
    pguid = forms.CharField()
    kw = forms.CharField(required=False)   
    
    def __init__(self, *callback_args, **callback_kwargs):
        BaseForm.__init__(self, *callback_args, **callback_kwargs)
    

class IndexForm(BaseForm):
    cityname = forms.CharField(initial="北京", required=False)
    kw = forms.CharField(required=False)
    
    def __init__(self, *callback_args, **callback_kwargs):
        BaseForm.__init__(self, *callback_args, **callback_kwargs)    
        
if __name__ == "__main__":
    form = SearchForm({"kw":"zhongguancun", "cityname":u"中关村"}, auto_id=False)
    #print form.kw
    formindex = IndexForm()
    print formindex
    
    #print form.is_valid()
    #print form
    
