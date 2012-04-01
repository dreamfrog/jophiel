'''
Created on 2012-3-23

@author: lzz
'''
from jophiel import app
from .base import BaseQueue

"""
The ResQ class defines the Redis server object to which we will
enqueue jobs into various queues.
"""
class SimpleMessageQueue(object):

    def __init__(self,conn,queue):
        self.conn = conn
        self.client = self.conn.SimpleQueue(queue)
        self.serialize  = "json"
        self.headers=None
        self.compression=None
        self.routing_key=None
    
    @classmethod
    def instance(cls,queue):
        base = BaseQueue.instance()
        return cls(base.conn,queue)
    
    #item should map type
    def push(self, item):
        self.client.put(item, serializer=self.serialize, 
                        headers=self.headers, compression = self.compression,
                        routing_key = self.routing_key)
    
    def pop(self, block=True, timeout=None):
        return self.client.get(block = block, timeout = timeout)
 
    def size(self):
        return int(self.client.qsize())
    
    def close(self):
        self.client.close()
        super(SimpleMessageQueue,self).close()
    
    

    
        
