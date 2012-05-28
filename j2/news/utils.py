'''
Created on 2012-4-11

@author: lzz
'''
import urllib2
import httplib2

from jophiel.contrib.scrapely import extractors,htmlpage
from jophiel.contrib.readability import Document
from .models import ExtractResults

from scrapy.http import HtmlResponse
from scrapy.contrib.linkextractors.lxmlhtml import LxmlParserLinkExtractor
from scrapy.utils.url import parse_url
from scrapy.utils.url import canonicalize_url
from scrapy.utils.url import url_is_from_any_domain

from celery.task import task
from celery.task.sets import TaskSet

import urlparse
from jophiel.contrib.scrapely import extractors
from jophiel.contrib import html2text

def get_url_domain(url):
    host_name = parse_url(url).hostname
    if host_name.startswith("www."):
        return host_name[4:]
    else:
        return host_name
    
def extract_content(body,encoding="utf-8"):    
    document = Document(body)
    summary = document.summary()
    title = document.title()
    html= extractors.htmlregion(summary)
    t = lambda s: extractors.text(extractors.htmlregion(s))
    #text = html2text.html2text(html)
    return summary.encode(encoding),t(html).encode(encoding),title.encode(encoding) 

def save_content(url,summary,text,title):
    result,_ = ExtractResults.objects.get_or_create(url = url)
    result.content = text
    result.title = title
    result.summary = summary
    result.save()    

def fetch_body(url):
    req = httplib2.Http()
    reps,content = req.request(url)
    if reps.status == 200:
        return content
    return None    
       
def fetch_content(url,body):
    try:
        return extract_content(body)
    except Exception, exc:
        import traceback
        traceback.print_exc()
        print("URL %r gave error: %r" % (url, exc))
    return (None,None,None)

def fetch_url_content(url):
    content = fetch_body(url)
    if content:
        return fetch_content(url,content)
    return None
    
def url_first_page_fetch(url):
    req = httplib2.Http()
    reps,content = req.request(url)
    domain = get_url_domain(url)
    if reps.status == 200 :
        results = set()
        results.add(url)
        response = HtmlResponse(url,status = reps.status,
                                body = content,headers = reps)
        extractor = LxmlParserLinkExtractor()
        links = extractor.extract_links(response)
        for link in links:
            if url_is_from_any_domain(link.url,(domain,)):
                results.add(link.url)
        return results
    return []
