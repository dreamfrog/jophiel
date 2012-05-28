'''
Created on 2012-5-19

@author: lzz
'''
from .tables import RequestTable
from jophiel.crawler.http import Request

from sqlalchemy.dialects.oracle.zxjdbc import ReturningParam
from sqlalchemy.engine import base, default
from sqlalchemy.engine.base import Connection, Engine

from sqlalchemy import MetaData, Integer, String, INT, VARCHAR, func, \
    bindparam, select, event, TypeDecorator, create_engine, Sequence
from sqlalchemy.sql import column, literal
from sqlalchemy import *

def inset():
    start_urls = [
            "http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html",
         ]
    table = RequestTable("tests")
    for url in start_urls:
        request = Request(url)
        table.store_request(request)
    #for value in table.select():

users, metadata = None, None
db  = create_engine("mysql://root:zhong@localhost/jophiel")

def go(conn):
    for value in conn.execute("select * from users"):
        print value
    conn.execute('insert into zhong_time (user_name) values ("zhong")')

def tt():
    global users, metadata

    metadata = MetaData(db)
    users = Table('zhong_time', metadata,
        Column('user_name', VARCHAR(20)),
    )     
    metadata.create_all()

    table = RequestTable("tests_zhong_yyy__xxx") 
    request = Request("http://httplib2.googlecode.com/hg/doc/html/libhttplib2.html")  
   
    values = {
              "request_path":request.request_path,
              "url":request.url,
              "method":request.method,
              "body":request.body,
              } 
 
    conn = db.connect()
    try:
        go(conn)
        ins = table.table.insert()
        table.engine.execute(ins,**values)
        
    finally:
        conn.close()