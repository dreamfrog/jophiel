'''
Created on 2012-5-10

@author: lzz
'''
import datetime

from jophiel.crawler.utils.url import canonicalize_url
from jophiel.crawler.w3lib.http import headers_dict_to_raw,headers_raw_to_dict
from jophiel.crawler.http import Headers
from jophiel.crawler.http import Request
from jophiel.crawler.responsetypes import responsetypes
from jophiel.storage.columns import ColumnsField
from jophiel.storage.columns import BaseModel
from jophiel.storage.tables import BaseTable

from sqlalchemy import *

class RequestStat(object):
    STAT_NEED_DOWNLOAD = 0
    STAT_DOWNLOADED = 1
    STOP_DOWNLOAD = 2
    
class RequestTable(BaseTable):

    id = Column(Integer, autoincrement = True,primary_key = True)
    request_path = Column(String(64),nullable = False,index = True,unique = True)
    
    url = Column(String(255), nullable = False)
    method = Column(String(16),nullable = False,default = "GET")
    body = Column(Text(),nullable = False,default = "")
    response_url  = Column(String(255), nullable = False,default="")
    domain = Column(String(255),default="")

    refer_id = Column(Integer,nullable=False,default = 0)        
    request_headers = Column(Text(),default="")
    response_headers = Column(Text(),default="")
    
    status = Column(Integer, nullable = False,default=0)
    type = Column(String(20),default = "")
    download_times = Column(Integer,nullable = False,default = 0)
    last_error_times = Column(Integer,nullable = False,default = 0)
    state = Column(Integer,nullable = False,default = 0) 
    
    create_time = Column(DateTime, default=func.now())
    lastupdate_time = Column(DateTime, nullable = False,default=func.now())  
    
    #schedule_time = Column(DateTime,nullable = True)

    def store_request(self,request):
        values = {
                  "request_path":request.request_path,
                  "url":request.url,
                  "method":request.method,
                  "body":request.body,
                  "request_headers":headers_dict_to_raw(request.headers)
                  }
        where = {
                 "request_path":request.request_path
                 }
        if not self.fetch_one(where,"request_path"):
            self.insert(**values)
        else:
            self.update(where,**values)
            
    def update_stat(self,request,stat):
        where = {
                 "request_path":request.request_path
                 }
        values = {
                  "state":stat
                  }
        self.update(where,**values)
    
    def fetch_status(self,stat = None,offset=None,limit=None):
        where = {}
        if not stat is None:
            where = {
                     "state":stat
                     }
        for result in self.iter_items(where,offset=offset,limit=limit):
            yield result
    
    def iter_requests(self,stat =None,offset=None,limit=None):
        requests = []
        for value in self.fetch_status(stat,offset=offset,limit=limit):
            request = Request(value["url"], method=value["method"], 
                              headers=Headers(headers_raw_to_dict(value["request_headers"]))) 
            requests.append(request)
        return requests     
        
    
    def update_response(self,response):
        request = response.request
        values = {
                  "status":response.status,
                  "response_headers":headers_dict_to_raw(response.headers),
                  "response_url":response.url,
                  "lastupdate_time":datetime.datetime.now(),
                  "state":RequestStat.STAT_DOWNLOADED,
                  }
        where = {
                 "request_path":request.request_path
                 }
        self.update(where,**values)
        
    @classmethod
    def storage_response(cls,spider,request,response):
        if not response.request:
            response.request = request
        table = RequestTable(spider.tablename)
        table.update_response(response)
        
        
