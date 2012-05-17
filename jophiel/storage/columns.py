'''
Created on 2012-5-13

@author: lzz
'''

from .backends.hbase_proxy import Datastore
from collections import defaultdict

class ColumnsField(object):
    def __init__(self, **kwargs):
        self.values = {}
     
        
class ModelDescriptor(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelDescriptor, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelDescriptor)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)
        
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
            
        fields = []
        for obj_name, obj in attrs.iteritems():
            if isinstance(obj, ColumnsField):
                fields.append((obj_name, obj))
                 
        setattr(new_class,"columns",fields)

        # Add all attributes to the class.
        for obj_name, obj in attrs.iteritems():
            setattr(new_class, obj_name, obj)

        return new_class

class BaseModel(object):
    
    __metaclass__ = ModelDescriptor

    def __init__(self,table_name,**kwargs):
        self.table_name = table_name
        self.__db = None
    
    def gen_schema(self):
        columns = []
        for column in self.columns:
            value = {
                     "name":column[0]
                     }
            columns.append(value)
        return columns
     
    @property
    def columns_name(self):
        columns = []
        for name,value in self.columns:
            columns.append(name)
        return columns
          
    @property
    def db(self):
        if not self.__db:
            self.__db = Datastore()
            if not self.__db.table_exist(self.table_name):
                schemas = self.gen_schema()
                self.__db.create_table(self.table_name, schemas)
        return self.__db
    
    def __eq__(self, other):
        return type(other) == type(self) and other.table_name ==self.table_name

    def __repr__(self):
        return u'<%s: %s>,<%s:%s>' % (self.__class__.__name__, unicode(self),self.table_name,self.pk)

    def __unicode__(self):
        return self.pk or u'None'

    def save(self,row_key,**values):
        self.update(row_key,**values)       

    def update(self,row_key, **values):   
        model = self.table_name
        columns = {}
        for key,item in values.items():
            if isinstance(item,dict):
                for second,value in item.items():
                    if isinstance(value,list):
                        value  = value[0]
                    columns[key+":"+second] = value
        result = self.db.put_entity(model,row_key, columns)
        return result

    def fetch(self,row_key,*columns):
        rets = defaultdict(dict)
        results = self.db.get_entity(self.table_name, row_key, columns)
        if results:
            for values in results:
                for key,value in values.items():
                    if ":" in key:
                        family,column = key.split(":")
                        rets[family][column] = value
                    else:
                        rets[key][":"] = value
        return rets
     
                    
    

