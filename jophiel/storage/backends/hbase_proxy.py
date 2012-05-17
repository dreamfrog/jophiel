
import os
import time

from thrift.transport import TSocket,TTransport
from thrift.protocol import TBinaryProtocol

from .hbase import Hbase
from .hbase import ttypes

import threading
import logging
from django.conf import settings

from .base import BaseBackend
from .base import IllegalParameters
from .pool import ConnectionPool

logger = logging.getLogger(__name__)

def log_time(func):
    debug = True
    def new_func(*args, **kwargs):
        if not debug: 
            return func(*args, **kwargs)
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        logger.debug(str(func) + ": " + str(end_time - start_time) + " s")
        return result
     
    return new_func

pool = ConnectionPool(server_list=[settings.HBASE_THRIFT_HOST,])

DEFAULT_MAX_VERSIONS = settings.HBASE_DEFALT_MAX_VERSIONS

class Datastore(BaseBackend):

    def __init__(self):
        self.__connection = None
    
    def close(self):
        if self.__connection:
            self.__connection.return_to_pool()
        self.__connection = None

    @property
    def connection(self):
        if not self.__connection:
            self.__connection = pool.get()
        return self.__connection
    
    def get_schema(self, table_name):
        elist = [] 
        if not table_name:
            raise IllegalParameters()
        
        client = self.connection
        try:
            keys = (client.getColumnDescriptors(table_name)).keys()
            # Last character has ":" for version 89 and up, remove it
            for index, ii in enumerate(keys):
                keys[index] = ii[:-1] 
            elist.extend(keys)
        except ttypes.IOError, io:
            logger.error("Get Schema IO Error--" + io.message)
        return elist
    
    def get_row_count(self, table_name):
        raise NotImplementedError("not implemented")
    
    def create_table(self, table_name, family_columns):
        client = self.connection
        columnlist = []
        for column in family_columns:
            col = ttypes.ColumnDescriptor()
            col.name = column["name"] + ":"
            col.maxVersions = column["max_version"] if "max_version" in column \
                    else DEFAULT_MAX_VERSIONS
            columnlist.append(col)
        client.createTable(table_name, columnlist)

    def table_exist(self, table_name):
        ret = False
        try:
            client = self.connection
            tables = client.getTableNames()
            if table_name in tables:
                ret = True
        except:
            ret = False
                 
        return ret
    
    def delete_table(self, table_name):
        elist = [] 
        if not table_name:
            logger.error("Illegal Argument: param should not be empty in put %s" \
                 %(table_name)) 
            raise IllegalParameters
        
        client = self.connection
        try:
            client.disableTable(table_name)
            client.deleteTable(table_name)
        except ttypes.IOError, io:
            logger.error("IOError in delete_table : %s in put %s"
                         %(str(io),table_name))                
        return elist
    
    def put_entity(self, table_name, row_key,column_values):
        elist = []
        if (not row_key) or (not table_name) or (not column_values):
            logger.error("Illegal Argument: param should not be empty in put %s %s %s" \
                         %(table_name,row_key,str(column_values))) 
            raise IllegalParameters
        
        client = self.connection
        try:
            mutations = []      
            for column_name,column_value in column_values.items():
                m = ttypes.Mutation()
                m.column = column_name + ":" if ":" not in column_name else column_name                    
                m.value = column_value
                mutations.append(m)
            client.mutateRow(table_name, row_key, mutations)
        except ttypes.IOError, io:
            logger.error("IOError: %s in put %s %s %s"
                         %(str(io),table_name,row_key,str(column_values)))
        #print "exception type: IOError"
        except ttypes.IllegalArgument, io:
            logger.error("Illegal Argument: %s in put %s %s %s"
                         %(str(io),table_name,row_key,str(column_values))) 
        return elist
    
    def get_entity(self, table_name, row_key, column_names):
        elist = [] 
        if not table_name or not row_key or not column_names:
            logger.error("Illegal Argument: param should not be empty in put %s %s" \
                 %(table_name,row_key)) 
            raise IllegalParameters
        
        client = self.connection
        try:
            column_list = []

            for name in column_names:
                column_name = name +":" if ":" not in name else name
                column_list.append(column_name) 
            column_results = client.getRowWithColumns(table_name, row_key, column_list)
            values = {}
            for columns in column_results:
                for column_name,cell in columns.columns.items():
                    values[column_name] = cell.value
            if values:
                elist.append(values)
                    
        except ttypes.IOError, io:
            logger.error("IOError: %s in get %s %s %s"
                         %(str(io),table_name,row_key,str(column_names)))
            
        return elist

    def get_row(self, table_name, row_key):
        values = {}
        if not table_name or not row_key:
            logger.error("Illegal Argument: param should not be empty in put %s %s" \
                 %(table_name,row_key)) 
            raise IllegalParameters
        
        client = self.connection
        try:
            rows = client.getRow(table_name, row_key)
            for row in rows:
                for key,cell in row.columns.items():
                    key=key.strip(":")
                    values[key] = cell.value    
                
        except ttypes.IOError, io:
            logger.error("IOError: %s in put %s %s"%(str(io),table_name,row_key)) 
            
        return values

    def delete_row(self, table_name, row_key):
        if not table_name or not row_key:
            logger.error("Illegal Argument: param should not be empty in put %s %s" \
                 %(table_name,row_key)) 
            raise IllegalParameters
        
        client = self.connection
        try: 
            client.deleteAllRow(table_name, row_key)
        except ttypes.IOError, io:
            logger.error("IOError: %s in get %s %s"
                         %(str(io),table_name,row_key))

    def items(self, table_name, column_families):
        elist = []
        default_each_row_num = 10
        if not table_name or not column_families:
            logger.error("Illegal Argument: param should not be empty in put %s %s" \
                 %(table_name,column_families)) 
            raise IllegalParameters
        
        client = self.connection
        try: 
            columnNames = []
            for col in column_families:
                columnNames.append(col + ":")
                
            scanner = client.scannerOpen(table_name, "", columnNames) 
            r = client.scannerGetList(scanner,default_each_row_num)
            while r:
                result = {}
                for row_result in r:
                    values = {}
                    for column_name,cell_value in row_result.columns.items():
                        values[column_name] = cell_value
                    result[row_result.row] = values
                elist.append(result)
                r = client.scannerGetList(scanner,default_each_row_num)
            client.scannerClose(scanner) 
        except ttypes.IOError, io:
            logger.error("IOError: %s in get %s %s"%(str(io),table_name,column_families))
        except ttypes.IllegalArgument, e:
            logger.error("IllegalArgument: %s in get %s %s"%(str(e),table_name,column_families))
        return elist  

    def iter_items(self, table_name, column_families):
        default_each_row_num = 10
        if not table_name or not column_families:
            logger.error("Illegal Argument: param should not be empty in put %s %s" \
                 %(table_name,column_families)) 
            raise IllegalParameters
        
        client = self.connection
        try: 
            columnNames = []
            for col in column_families:
                columnNames.append(col + ":")
                
            scanner = client.scannerOpen(table_name, "", columnNames) 
            rows = client.scannerGetList(scanner,default_each_row_num)
            while rows:
                result = {}
                for row_result in rows:
                    values = {}
                    for column_name,cell_value in row_result.columns.items():
                        values[column_name] = cell_value
                    result[row_result.row] = values
                
                yield result
                rows = client.scannerGetList(scanner,default_each_row_num)
            client.scannerClose(scanner) 
        except ttypes.IOError, io:
            logger.error("IOError: %s in get %s %s"%(str(io),table_name,column_families))
        except ttypes.IllegalArgument, e:
            logger.error("IllegalArgument:%s %s in get %s %s"%(str(e),table_name,column_families))