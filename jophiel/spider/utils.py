'''
Created on 2012-5-11

@author: lzz
'''
import json
from .tables import RequestTable
from .models import Spider

from jophiel.crawler.http import Request

def indert_form(model,form_data):
    columns = {}
    for key,value in form_data.items():
        if hasattr(model,key):
            columns[key] = value
    model.save(**columns)

def create_seed_request(spider,url_json): 
    #store seed urls
    table = RequestTable(spider.tablename)
    urls = json.loads(url_json)
    for url in urls:
        request = Request(url = url)
        table.store_request(request)

from jophiel.schedule.utils import create_internal_task

def create_spider_task(spider):
    create_internal_task(spider.name,"tasks.schedule_spider_task",5,spider.name)

