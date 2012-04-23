'''
Created on 2012-3-19

@author: lzz
'''
from .base import BaseBackend

class DatastoreProxy(BaseBackend):
    key_name = "row_key"
    def get_schema(self, table_name):pass
    def get_row_count(self, table_name):pass
    
    def create_table(self, table_name, family_columns):pass
    def table_exist(self, table_name):pass
    def delete_table(self, table_name):pass
    def put_entity(self, table_name, row_key,column_values):pass
    def get_entity(self, table_name, row_key, column_names):pass
    def get_row(self, table_name, row_key):pass
    def delete_row(self, table_name, row_key):pass
    def items(self, table_name, column_families):pass
    def iter_items(self, table_name, column_families):pass
