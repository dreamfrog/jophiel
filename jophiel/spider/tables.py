'''
Created on 2012-5-10

@author: lzz
'''
from jophiel.storage.tables import BaseTable
from sqlalchemy import *

class RequestTable(BaseTable):

    request_id = Column(Integer, autoincrement = True,primary_key = True)
    request_path = Column(String(64),nullable = False,index = True,unique = True)
    
    url = Column(String(255), nullable = False)
    method = Column(String(16),nullable = False,default = "GET")
    body = Column(Text(),nullable = False,default = "")
    source_id = Column(Integer,nullable=False,default = 0)
    response_url  = Column(String(16), nullable = False,default="")
    domain = Column(String(255),default="")
    
    request_headers = Column(Text(),default="")
    response_headers = Column(Text(),default="")
    
    status = Column(String(20), nullable = False,default="")
    type = Column(String(20),default = "")

    create_time = Column(DateTime, default=func.now())
    #lastupdate_time = Column(DateTime, nullable = False)  
    #schedule_time = Column(DateTime,nullable = True)
