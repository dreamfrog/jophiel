'''
Created on 2012-4-13

@author: lzz
'''
import time 
import datetime

from .encoding import  utf8
from . import dateutil

class TypeItem:

    STRING = "string"
    DATE   = "date"
    NULL   = "null"

    def __init__(self):
        self._type = {}
        self._value = {}

    def values(self):
        return self._value
    
    def has_key(self, key):
        """Check whether the key exists."""
        key = key.replace(" ", "_")
        return self._value.has_key(key)

    def key_type(self, key):
        """Return the key type."""
        key = key.replace(" ", "_")
        return self._type[key]

    def set(self, key, value):
        """Set the value of the given key.
        """
        key = key.replace(" ", "_")

        try:
            func = getattr(self, "set_" + key)
        except AttributeError:
            pass
        else:
            return func(key, value)

        if value == None:
            return self.set_as_null(key, value)
        else:
            try:
                return self.set_as_string(key, value)
            except TypeError:
                return self.set_as_date(key, value)

    def get(self, key):
        """Return the value of the given key.
        """
        key = key.replace(" ", "_")
        try:
            func = getattr(self, "get_" + key)
        except AttributeError:
            pass
        else:
            return func(key)

        try:
            func = getattr(self, "get_as_" + self._type[key])
        except AttributeError:
            pass
        else:
            return func(key)

        return self._value[key]

    def set_as_string(self, key, value):
        """Set the key to the string value.
        """
        value = utf8(value)
        key = key.replace(" ", "_")
        self._value[key] = value
        self._type[key] = self.STRING

    def get_as_string(self, key):
        """Return the key as a string value."""
        key = key.replace(" ", "_")
        if not self.has_key(key):
            raise KeyError, key
        return self._value[key]

    def set_as_date(self, key, value):
        """Set the key to the date value.
        The date should be a 9-item tuple as returned by time.gmtime().
        """
        key = key.replace(" ", "_")
        self._value[key] = value
        self._type[key] = self.DATE

    def get_as_date(self, key):
        """Return the key as a date value."""
        key = key.replace(" ", "_")
        if not self.has_key(key):
            raise KeyError, key
        value = self._value[key]
        return dateutil.get_as_date(value)

    def set_as_null(self, key, value):
        """Set the key to the null value.
        """
        key = key.replace(" ", "_")
        self._value[key] = ""
        self._type[key] = self.NULL

    def get_as_null(self, key):
        """Return the key as the null value."""
        key = key.replace(" ", "_")
        if not self.has_key(key):
            raise KeyError, key

        return None

    def del_key(self, key):
        """Delete the given key."""
        key = key.replace(" ", "_")
        if not self.has_key(key):
            raise KeyError, key

        del(self._value[key])
        del(self._type[key])

    def keys(self):
        """Return the list of cached keys."""
        return self._value.keys()

    def __iter__(self):
        """Iterate the cached keys."""
        return iter(self._value.keys())

    # Special methods
    __contains__ = has_key
    __setitem__  = set_as_string
    __getitem__  = get
    __delitem__  = del_key
    __delattr__  = del_key

    def __setattr__(self, key, value):
        if key.startswith("_"):
            self.__dict__[key] = value
        else:
            self.set(key, value)

    def __getattr__(self, key):
        if self.has_key(key):
            return self.get(key)
        else:
            raise AttributeError, key

    def save_attr(self,obj):
        values  = self.values()
        for key in values.keys():
            if hasattr(obj,key):
                setattr(obj,key,self.get(key))