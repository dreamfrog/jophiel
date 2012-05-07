
import sys
import time

from thrift import Thrift
from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from storage.hbase import ttypes
from storage.hbase.Hbase import Client, ColumnDescriptor, Mutation

from storage.connection import Connection


client = Connection("localhost:9090")

t = "demo_table"

#
# Scan all tables, look for the demo table and delete it.
#
print "scanning tables..."
for table in client.getTableNames():
  print "  found: %s" %(table)
  if table == t:
    if client.isTableEnabled(table):
      print "    disabling table: %s"  %(t)
      client.disableTable(table)
    print "    deleting table: %s"  %(t)
    client.deleteTable(table)

columns = []
col = ColumnDescriptor()
col.name = 'entry:'
col.maxVersions = 10
columns.append(col)
col = ColumnDescriptor()
col.name = 'unused:'
columns.append(col)

try:
  print "creating table: %s" %(t)
  client.createTable(t, columns)
except AlreadyExists, ae:
  print "WARN: " + ae.message
