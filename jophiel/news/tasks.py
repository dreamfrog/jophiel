'''
Created on 2012-4-9

@author: lzz
'''

from celery.task import task
import urllib2
from jophiel.contrib.readability import Document

from .models import ExtractResults
from .utils import fetch_content,save_content,fetch_body
from .utils import url_first_page_fetch
from . import utils

@task(ignore_result=True, serializer="pickle", compression="zlib")
def extract_content(url,body):
    summary,text,title = utils.extract_content(body)
    if text.strip() and title.strip():
        save_content(url,summary,text,title)

@task(ignore_result=True, serializer="pickle", compression="zlib")
def url_content_extract(urls):
    for url in urls:
        body = fetch_body(url)
        extract_content.delay(url,body)
             
@task(ignore_result=True, serializer="pickle", compression="zlib")
def url_extract_task(url):
    results = url_first_page_fetch(url)
    if results:
        url_content_extract.apply_async(args=(results,))
        

    
    