'''
Created on 2012-5-10

@author: lzz
'''
from sqlalchemy import *
from alchemy import *
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
        if name not in self.metadata:
            table = Table(name,self.metadata,*columns)
            self.metadata.create_all(self.engine)
        else:
            table = self.metadata.tables[name]
        return table
    
    @property
    def table(self):
        if self._table ==None:
            columns = copy.deepcopy(self.columns)
            self._table = self.get_or_create_table(self.table_name ,columns) 
        return self._table
    
    def insert(self,**kwargs):
        ins = self.table.insert()
        self.engine.execute(ins,**kwargs).close()
        
    def update(self,wheres,**kwargs):
        ups = self.table.update().values(**kwargs).execution_options(autocommit=True)
        for key ,item in wheres.items():
            ups = ups.where(self.table.c[key] == item)
        self.engine.execute(ups).close()
    
    def iter_items(self,where={},offset=None,limit=None,*args):
        columns = []
        for item in args:
            columns.append(self.table.c[item])
        columns = [self.table]
        sl = select(columns)
        if offset:
            sl = sl.offset(offset)
        if limit:
            sl = sl.limit(limit)
              
        for key,value in where.items():
            sl = sl.where(self.table.c[key]==value)
        results = self.engine.execute(sl)
        for result in results:
            yield result 
 
    def count_items(self,wheres={}):
        columns = [func.count(self.table.c.id)]
        sl = select(columns) 
        print sl             
        for key,value in wheres.items():
            sl = sl.where(self.table.c[key]==value)
        return self.engine.execute(sl).scalar()
  
    def fetch_one(self,wheres,*args):
        columns = []
        for item in args:
            columns.append(self.table.c[item])
        columns = [self.table]
        sl = select(columns)
        for key,value in wheres.items():
            sl = sl.where(self.table.c[key]==value)
        return self.engine.execute(sl).fetchone()
        
    