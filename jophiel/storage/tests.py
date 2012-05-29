'''
Created on 2012-5-29

@author: lzz
'''
'''
Created on 2012-5-7

@author: lzz
'''

import sys
import time

from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from jophiel.storage.backends.hbase import ttypes
from jophiel.storage.backends.hbase.Hbase import Client, ColumnDescriptor, Mutation
from jophiel.storage.backends.connection import Connection
from jophiel.storage.backends.hbase_backend import Datastore
from django.utils import unittest


class TestModels(unittest.TestCase):
    table_name= "demo_table"
    
    def setUp(self):
        client = Connection("localhost:9090")
        print "scanning tables..."
        for table in client.getTableNames():
            if table == self.table_name:
                if client.isTableEnabled(table):
                    client.disableTable(table)
                client.deleteTable(table)
        client.close()    
          
    def testBasicStorage(self):
        store = Datastore()
        webpage = self.table_name
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
        self.assertEqual(len(result),1)
        self.assertIn("headers:auth",result[0])
        self.assertEqual(result[0]["headers:auth"],"firefox")
        
        store.delete_table(webpage)


