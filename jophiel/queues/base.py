'''
Created on 2012-3-23

@author: lzz
'''

import json
from jophiel.backend.connection import BrokerConnection
from jophiel import settings

class TaskMessage(object):
    @classmethod
    def encode(cls, item):
        return json.dumps(item)

    @classmethod
    def decode(cls, item):
        if isinstance(item, basestring):
            ret = json.loads(item)
            return ret
        return None

class BaseQueue(object):
    conn = None
    
    def __init__(self,conn):
        self.conn = conn
    
    @classmethod
    def instance(cls):
        backend = settings.QUEUE_BACKEND
        if not cls.conn:
            conn = BrokerConnection(backend)
            return cls(conn)
        return cls(cls.conn)
        
    def close(self):
        self.conn.close()