import datetime
import simplejson

try:
    import cPickle as pickle
except ImportError:
    import pickle
import uuid

class Field(object):
    def __init__(self, default=None, **kwargs):
        self.default = default

    def get_default(self):
        if not self.default:
            value = self.to_python(None)
        elif callable(self.default):
            value = self.default()
        else:
            value = self.default
        return value

    def to_db(self, value=None):
        if value is None:
            value = ''
        return value

    def to_python(self, value=None):
        return value

class KeyField(Field):
    
    def generate_key(self):
        return uuid.uuid4().hex
    
    def get_default(self):
        if not self.default:
            value = self.to_python(None)
        elif callable(self.default):
            value = self.default()
        else:
            value = self.default
        return value

    def to_python(self, value=None):
        if not value:
            value = self.generate_key()
        return value

class StringField(Field):
    def to_python(self, value=None):
        if value:
            value = unicode(value)
        else:
            value = u''
        return value

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

class DateTimeField(Field):
    def to_db(self, value=None):
        if isinstance(value, datetime.datetime):
            # TODO: coerce this to UTC
            value = value.isoformat()
        return value

    def to_python(self, value=None):
        if value and not isinstance(value, datetime.datetime):
            # TODO: coerce this to a UTC datetime object
            if '.' in value:
                value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                value = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
                
        return value

    def get_default(self):
        if not self.default:
            value = self.to_python(datetime.datetime.now())
        elif callable(self.default):
            value = self.default()
        else:
            value = self.default
        return value

class ListField(Field):
    def to_db(self, value=None):
        if isinstance(value, (tuple, list)):
            value = pickle.dumps(value)
        return value

    def to_python(self, value=None):
        if not value:
            value = []
        elif isinstance(value, basestring):
            value = pickle.loads(value)
        return value

class ReverseUrlField(Field):
    def to_db(self,value=""):
        return self.__reverse_url(value)
        
    def to_python(self,value=None):
        return self.__restore_url(value)

    def __reverse_url(self, url):
        protocol,link = filter(None, url.split("//"))
        hops = filter(None, link.split("/"))  
        domain = hops[0].split(".")  
        domain.reverse()  
        domain = '.'.join(domain)  
        hops[0] = domain  
        return protocol + "//"+'/'.join(hops) 
     
    def __restore_url(self,url):
        prococol,link = filter(None, url.split("//"))[-1]  
        hops = filter(None, link.split("/"))  
        domain = hops[0].split(".")  
        domain.reverse()  
        domain = '.'.join(domain)  
        hops[0] = domain  
        return prococol + "//"+'/'.join(hops)      


def to_db(model, values):
    result = {}
    for k, v in values.iteritems():
        field = model._meta.fields.get(k)
        if field:
            v = field.to_db(v)
            if v is None:
                v = ''
        else:
            v = simplejson.dumps(v)
        result[k] = v
    return result        