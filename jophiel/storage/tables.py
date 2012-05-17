'''
Created on 2012-5-10

@author: lzz
'''
from sqlalchemy import *
from sqlalchemy.sql import select

from .aldjemy.core import *
import copy 

class TableDescriptor(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(TableDescriptor, cls).__new__
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})

        # Add all attributes to the class.
        fields = []
        for obj_name, value in attrs.iteritems():
            if isinstance(value,Column):
                obj = copy.deepcopy(value)
                obj.key = obj.name= obj_name
                print obj,obj.key,obj
                setattr(new_class, obj_name, obj)
                fields.append(obj)
            else:
                setattr(new_class,obj_name,value)
        setattr(new_class,"columns",fields)
        return new_class
    

class BaseTable(object):
    
    __metaclass__  = TableDescriptor
    
    def __init__(self,table_name):
        self.table_name = table_name
        self.metadata = get_meta()
        self.engine = get_engine()
        self._table = None
        
    def get_or_create_table(self,name,columns):
        metadata = get_meta()
        engine = get_engine()
        if name not in metadata:
            table = Table(name,metadata,*columns)
            metadata.create_all(engine)
        else:
            table = metadata.tables[name]
        return table
    
    @property
    def table(self):
        if self._table ==None:
            self._table = self.get_or_create_table(self.table_name ,self.columns) 
        return self._table
    
    def insert(self,**kwargs):
        ins = self.table.insert()
        result = self.engine.execute(ins,**kwargs)
        
    def update(self,wheres,**kwargs):
        ups = self.table.update().values(**kwargs)
        for key ,item in wheres.items():
            ups = ups.where(self.table.c[key] == item)
        result = self.engine.execute(ups)
    
    def select(self,wheres={},*args):
        columns = []
        for item in args:
            columns.append(self.table.c[item])
        columns = self.columns if not columns else columns
        sl = select(columns)
        for key,value in wheres.items():
            sl = sl.where(self.table.c[key]==value)
        result = self.engine.execute(sl)
        return result  
    
    def fetch_one(self,where,*args):pass
        
    