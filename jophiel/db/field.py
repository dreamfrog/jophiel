import datetime
import simplejson

try:
    import cPickle as pickle
except ImportError:
    import pickle

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

class ForeignKey(object):
    def __init__(self, to_model):
        self.to_model = to_model

class String(Field):
    def to_python(self, value=None):
        if value:
            value = unicode(value)
        else:
            value = u''
        return value

class Text(String):
    pass

class Integer(Field):
    def to_python(self, value=None):
        if value:
            value = int(value)
        else:
            value = 0
        return value

class Float(Field):
    def to_python(self, value=None):
        if value:
            value = float(value)
        else:
            value = 0.0
        return value

class DateTime(Field):
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

class List(Field):
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
