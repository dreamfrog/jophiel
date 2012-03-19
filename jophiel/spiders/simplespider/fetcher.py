'''
Created on 2012-3-6

@author: lzz
'''
import re
import sys
import time
import math
import urlparse
import optparse
import traceback
from cgi import escape

import BeautifulSoup

import eventlet
from eventlet.green import urllib2
httplib2 = eventlet.import_patched('httplib2')

from http import HTTPRequest
from http import HTTPResponse

# http://daringfireball.net/2009/11/liberal_regex_for_matching_urls
url_regex = re.compile(r'\b(([\w-]+://?|www[.])[^\s()<>]+(?:\([\w\d]+\)|([^[:punct:]\s]|/)))')

class Fetcher():
    def __init__(self,settings,input_queue,out_queue):
        self.settings = settings
        self.out_queue = out_queue
        self.url_queue =input_queue
        self.pool = eventlet.GreenPool()
        
        self.http = httplib2.Http()
        #self.http.force_exception_to_status_code = True
    
    def __fetch_url(self,request):
        headers  = request.headers
        body = request.body
        method = request.method
        uri = request.url
        resp, content = self.http.request(uri, method, body=body, headers=headers)
        print resp
    
    def __build_response(self,request,reps,content):
        response = HTTPResponse(request,reps.status,reps,content)
       
                
    def start(self):
        while not self.url_queue.empty() or self.pool.running() != 0:
            print  self.url_queue.empty()
            url = eventlet.with_timeout(0.1, self.url_queue.get, timeout_value='')
            # limit requests to eventlet.net so we don't crash all over the internet
            if url:
                self.pool.spawn_n(self.__fetch_url, url)
            
if __name__ =="__main__":
    setting = {}

    urls = [
         "http://www.google.com/intl/en_ALL/images/logo.gif",
         "https://wiki.secondlife.com/w/images/secondlife.jpg",
         "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif"
         ]
    requests = [HTTPRequest(url) for url in urls]
    out_queue = eventlet.Queue()
    url_queue = eventlet.Queue()
    for request in requests:
        url_queue.put(request)
        
    fetcher = Fetcher(setting,url_queue,out_queue)
    fetcher.start()
    
    while not out_queue.empty():
        print len(out_queue.get())
    
