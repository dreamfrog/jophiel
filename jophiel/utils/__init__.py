'''
Created on 2012-2-23

@author: lzz
'''
import os

from UserDict import DictMixin

try:
    from setproctitle import setproctitle
except:
    def setproctitle(name):
        pass

def my_import(name):
    """Helper function for walking import calls when searching for classes by
    string names.
    """
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def safe_str_to_class(s):
    """Helper function to map string class names to module classes."""
    lst = s.split(".")
    klass = lst[-1]
    mod_list = lst[:-1]
    module = ".".join(mod_list)
    mod = my_import(module)
    if hasattr(mod, klass):
        return getattr(mod, klass)
    else:
        raise ImportError('can not import %s' % s)

def str_to_class(s):
    """Alternate helper function to map string class names to module classes."""
    lst = s.split(".")
    klass = lst[-1]
    mod_list = lst[:-1]
    module = ".".join(mod_list)
    try:
        mod = __import__(module)
        if hasattr(mod, klass):
            return getattr(mod, klass)
        else:
            return None
    except ImportError:
        return None

def setup_pidfile(path):
    if not path:
        return
    dirname = os.path.dirname(path)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname)
    with open(path, 'w') as f:
        f.write(str(os.getpid()))


class OrderedDict(dict, DictMixin):

    def __init__(self, *args, **kwds):
        if len(args) > 1:
            raise TypeError('expected at most 1 arguments, got %d' % len(args))
        try:
            self.__end
        except AttributeError:
            self.clear()
        self.update(*args, **kwds)

    def clear(self):
        self.__end = end = []
        end += [None, end, end]         # sentinel node for doubly linked list
        self.__map = {}                 # key --> [key, prev, next]
        dict.clear(self)

    def __setitem__(self, key, value):
        if key not in self:
            end = self.__end
            curr = end[1]
            curr[2] = end[1] = self.__map[key] = [key, curr, end]
        dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        dict.__delitem__(self, key)
        key, prev, next = self.__map.pop(key)
        prev[2] = next
        next[1] = prev

    def __iter__(self):
        end = self.__end
        curr = end[2]
        while curr is not end:
            yield curr[0]
            curr = curr[2]

    def __reversed__(self):
        end = self.__end
        curr = end[1]
        while curr is not end:
            yield curr[0]
            curr = curr[1]

    def popitem(self, last=True):
        if not self:
            raise KeyError('dictionary is empty')
        key = reversed(self).next() if last else iter(self).next()
        value = self.pop(key)
        return key, value

    def __reduce__(self):
        items = [[k, self[k]] for k in self]
        tmp = self.__map, self.__end
        del self.__map, self.__end
        inst_dict = vars(self).copy()
        self.__map, self.__end = tmp
        if inst_dict:
            return (self.__class__, (items,), inst_dict)
        return self.__class__, (items,)

    def keys(self):
        return list(self)

    setdefault = DictMixin.setdefault
    update = DictMixin.update
    pop = DictMixin.pop
    values = DictMixin.values
    items = DictMixin.items
    iterkeys = DictMixin.iterkeys
    itervalues = DictMixin.itervalues
    iteritems = DictMixin.iteritems

    def __repr__(self):
        if not self:
            return '%s()' % (self.__class__.__name__,)
        return '%s(%r)' % (self.__class__.__name__, self.items())

    def copy(self):
        return self.__class__(self)

    @classmethod
    def fromkeys(cls, iterable, value=None):
        d = cls()
        for key in iterable:
            d[key] = value
        return d

    def __eq__(self, other):
        if isinstance(other, OrderedDict):
            return len(self) == len(other) and \
                   all(p == q for p, q in  zip(self.items(), other.items()))
        return dict.__eq__(self, other)

    def __ne__(self, other):
        return not self == other

import os
import time, datetime
import sys
import logging

def special_log_file(filename):
    if filename in ("stderr", "stdout"):
        return True
    if filename.startswith("syslog"):
        return True
    return False

def get_logging_handler(filename, procname, namespace=None):
    if namespace:
        message_format = namespace + ': %(message)s'
    else:
        message_format = '%(message)s'
    format = '%(asctime)s %(levelname)-8s ' + message_format

    if not filename:
        filename = "stderr"
    if filename == "stderr":
        handler = logging.StreamHandler(sys.stderr)
    elif filename == "stdout":
        handler = logging.StreamHandler(sys.stdout)
    elif filename.startswith("syslog"): # "syslog:local0"
        from logging.handlers import SysLogHandler
        facility_name = filename[7:] or 'user'
        facility = SysLogHandler.facility_names[facility_name]

        if os.path.exists("/dev/log"):
            syslog_path = "/dev/log"
        elif os.path.exists("/var/run/syslog"):
            syslog_path = "/var/run/syslog"
        else:
            raise Exception("Unable to figure out the syslog socket path")

        handler = SysLogHandler(syslog_path, facility)
        format = procname + "[%(process)d]: " + message_format
    else:
        try:
            from logging.handlers import WatchedFileHandler
            handler = WatchedFileHandler(filename)
        except:
            from logging.handlers import RotatingFileHandler
            handler = RotatingFileHandler(filename, maxBytes=52428800,
                                          backupCount=7)
    handler.setFormatter(logging.Formatter(format, '%Y-%m-%d %H:%M:%S'))
    return handler

def setup_logging(procname, log_level=logging.INFO, filename=None):
    if log_level == logging.NOTSET:
        return
    logger = logging.getLogger()
    logger.setLevel(log_level)
    handler = get_logging_handler(filename, procname)
    logger.addHandler(handler)
