'''
Created on 2012-2-16

@author: lzz
'''

from scrapy.conf import metas

class Field(object):
    def __init__(self, default=None, **kwargs):
        self.default = default
        self.name = None
        self.settings = {}
        
    def get_default(self):
        if not self.default:
            value = self.to_python(None)
        elif callable(self.default):
            value = self.default()
        else:
            value = self.default
        return value

    def to_form(self, value=None):
        if value is None:
            value = ''
        return value

    def get_setting_value(self):
        if self.name in self.settings:
            return self.settings[self.name]
        else:
            return None
    
    def to_value(self):
        value = self.get_setting_value()
        if value:
            return self.to_python(value)
        else:
            return self.get_default()
        
    def to_python(self, value=None):
        return value

class StringField(Field):
    def to_python(self, value=None):
        if value:
            value = unicode(value)
        else:
            value = u''
        return value

class BooleanField(Field):
    def to_python(self, value=None):
        if value:
            return True
        else:
            value = False
        return value

class HashField(Field):
    def to_python(self, value=None):
        return value if value else {}

class ListField(Field):
    def to_python(self, value=None):
        return value if value else []
    
class TextField(StringField):
    pass

class IntegerField(Field):
    def to_python(self, value=None):
        if value:
            value = int(value)
        else:
            value = 0
        return value

class FloatField(Field):
    def to_python(self, value=None):
        if value:
            value = float(value)
        else:
            value = 0.0
        return value
    
class Options(object):
    def __init__(self, name, module, meta, attrs):
        
        def class_name (module, name):
            module_name = name if module == "" or module == "__main__" else module + "." + name
            return module_name 
        default_name = meta.__dict__.get("name", None)
        self.name = default_name or class_name(module, name)
        
        fields = []
        for obj_name, obj in attrs.iteritems():
            if isinstance(obj, Field):
                fields.append((obj_name, obj))
                setattr(self, obj_name, obj)
                obj.module_name = self.name
                obj.field_name = obj_name
                
        self.settings = dict(fields)
    
class SettingsDescriptor(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(SettingsDescriptor, cls).__new__
        parents = [b for b in bases if isinstance(b, SettingsDescriptor)]
        if not parents:
            return super_new(cls, name, bases, attrs)

        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        attr_meta = attrs.pop('Meta', None)
        if not attr_meta:
            meta = getattr(new_class, 'Meta', None)
        else:
            meta = attr_meta
        #setattr(new_class, '_meta', Options(name,module,meta, attrs))
        
        default_name = meta.__dict__.get("name", None)
        setattr(new_class, "name", default_name or "%s.%s" % (module, name))
        
        fields = []
        for obj_name, obj in attrs.iteritems():
            if isinstance(obj, Field):
                fields.append((obj_name, obj))
                setattr(new_class, obj_name, obj)
                
        setattr(new_class, "fields", dict(fields))

        # Add all attributes to the class.
        for obj_name, obj in attrs.iteritems():
            setattr(new_class, obj_name, obj)

        return new_class

class SettingObject(object):
    
    __metaclass__ = SettingsDescriptor
    
    class Meta(object):pass
    
    def __init__(self, metas, *args, **argv):
        self.metas = metas
        self.settings = {}
        if self.name in metas:
            self.settings = metas[self.name]
        for name, field in self.fields.items():
            field.settings = self.settings
            field.name = name
    
        
