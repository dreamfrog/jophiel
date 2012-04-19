'''
Created on 2012-2-28

@author: lzz
'''
import hashlib
import uuid

class BaseBackend(object):
    def _get_schema_name(self, schema):
        return schema.__name__.lower()

    def _get_composite_key(self, **keys):
        return hashlib.md5(';'.join('%s=%s' % (k, v) for k, v in keys.iteritems())).hexdigest()

    def generate_key(self, schema):
        return uuid.uuid4().hex