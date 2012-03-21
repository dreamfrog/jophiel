"""
sentry.db.models
~~~~~~~~~~~~~~~~

:copyright: (c) 2010 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
    
from .query import QuerySet
from .field import Field
from .field import to_db
from .errors import *

from jophiel import app
    
class ManagerDescriptor(object):
    def __init__(self, manager):
        self.manager = manager

    def __get__(self, instance, type=None):
        if instance != None:
            raise AttributeError("Manager isn't accessible via %s instances" % type.__name__)
        return self.manager

class Manager(object):
    def __init__(self, model):
        self.model = model
    
    def get_query_set(self,table_name):
        return QuerySet(self.model,table_name)

    def filter(self, table_name,**kwargs):
        return QuerySet(self.model, table_name,filter_by=kwargs)

    def all(self,table_name):
        return self.get_query_set(table_name)

    def get(self,table_name, pk):
        data = app.db.get_row(table_name, pk)
        if data == []:
            raise DoesNotExist
        return self.model(table_name,pk, **data)

    def put(self,table_name,pk,**values):
        instance = self.model(table_name,pk,**values)
        instance.save()
        return instance

    def create_schema(self,table_name):
        if app.db.table_exist(table_name):
            return 
        app.db.create_table(table_name, self.model._meta.column_families) 

class Options(object):
    def __init__(self, meta, attrs):
        # Grab fields
        fields = []
        for obj_name, obj in attrs.iteritems():
            if isinstance(obj, Field):
                fields.append((obj_name, obj))
        
        self.column_families = getattr(meta,"columns_families",[])
        if not self.column_families:
            for attr_name,obj in fields:
                column_schema = {}
                column_schema["name"] = attr_name
                self.column_families.append(column_schema)
        
        self.fields = dict(fields)


class ModelDescriptor(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(ModelDescriptor, cls).__new__
        parents = [b for b in bases if isinstance(b, ModelDescriptor)]
        if not parents:
            # If this isn't a subclass of Model, don't do anything special.
            return super_new(cls, name, bases, attrs)
        
        print name,bases,attrs
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        
        attr_meta = attrs.pop('Meta', None)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta
        
        #key_name = "row_key"
        #if not key_name in attrs:
        #    raise Exception("key:[%s] item not in attrs:[%s]"%(key_name,attrs.keys()))
        #setattr(new_class,key_name,attrs.pop(key_name))
        
        setattr(new_class, '_meta', Options(meta, attrs))
        setattr(new_class, 'objects', Manager(new_class))

        # Add all attributes to the class.
        for obj_name, obj in attrs.iteritems():
            setattr(new_class, obj_name, obj)

        return new_class

class BaseModel(object):
    __metaclass__ = ModelDescriptor

    def __init__(self,table_name,pk = None,**kwargs):
        
        self.table_name = table_name
        
        for attname, field in self._meta.fields.iteritems():
            try:
                val = field.to_python(kwargs.pop(attname))
            except KeyError:
                val = field.get_default()
            setattr(self, attname, val)
        
        if pk:
            self.pk = self.row_key.to_python(pk)
        else:
            self.pk = self.row_key.get_default()
            
        if kwargs:
            raise ValueError('%s are not part of the schema for %s' % (', '.join(kwargs.keys()), self.__class__.__name__))

    def __eq__(self, other):
        return type(other) == type(self) and other.table_name ==self.table_name and other.pk == self.pk
    
    def __setattr__(self, key, value):
        field = self._meta.fields.get(key)
        if field and value:
            value = field.to_python(value)
        object.__setattr__(self, key, value)

    def __repr__(self):
        return u'<%s: %s>,<%s:%s>' % (self.__class__.__name__, unicode(self),self.table_name,self.pk)

    def __unicode__(self):
        return self.pk or u'None'

    def save(self):
        model = self.table_name
        values = dict((name, getattr(self, name)) for name in self._meta.fields.iterkeys())
        self.update(**values)       

    def update(self, **values):
        assert self.pk    
        model = self.table_name
        
        row_key = self.row_key.to_db(self.pk)
        print row_key,to_db(self, values)
        result = app.db.put_entity(model, self.pk, to_db(self, values))
        for k, v in values.iteritems():
            setattr(self, k, v)
        return self

    def delete(self):
        assert self.pk
        model = self.table_name
        app.db.delete_row(model, self.pk)

    

