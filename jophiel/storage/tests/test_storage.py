
import sys
import time

from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from jophiel.storage.hbase import ttypes
from jophiel.storage.hbase.Hbase import Client, ColumnDescriptor, Mutation
from jophiel.storage.connection import Connection
from jophiel.storage.hbase_backend import DatastoreProxy
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
        store = DatastoreProxy()
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
