'''
Created on 2012-5-11

@author: lzz
'''
from .tables import RequestTable
from .models import Spider

from jophiel.crawler.http import Request

def indert_form(model,form_data):
    columns = {}
    for key,value in form_data.items():
        if hasattr(model,key):
            columns[key] = value
    model.save(**columns)

def create_seed_request(spider,form):
    data = form.cleaned_data    
    #store seed urls
    for url in data.get("urls","").split():
        request = Request(url = url)
        table = RequestTable(data["name"])
        table.insert_request(request)
