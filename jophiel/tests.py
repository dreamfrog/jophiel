'''
Created on 2012-5-4

@author: lzz
'''

from django.utils import unittest

from .storage.hbase_backend import DatastoreProxy

class StoreTests(unittest.TestCase):
    def testBasic(self):
        
        store = DatastoreProxy()
        webpage = "webpage2"
        columns =[
                  {"name":"domain"},
                  {"name":"headers"},
                  {"name":"meta"},
                  {"name":"body"},
                  ]
        store.create_table(webpage, columns)
        values = {
                  "domain:first":"dianping.com",
                  "domain:sencond":"time",
                  "headers:auth":"firefox",
                  "headers:refer":"http://www.sina.com.cn"
                  }
        store.put_entity(webpage, "http://dianping",values)
        
        result = store.get_entity(webpage, "http://dianping", ["domain","headers"])
        print result
        store.delete_table(webpage)

