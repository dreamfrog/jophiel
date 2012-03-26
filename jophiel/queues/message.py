'''
Created on 2012-3-23

@author: lzz
'''
import json

from jophiel import app

from .base import BaseQueue

class Message(object):
    
    @classmethod
    def encode(cls, item):
        return json.dumps(item)

    @classmethod
    def decode(cls, item):
        if isinstance(item, basestring):
            ret = json.loads(item)
            return ret
        return None

class MessageQueue(BaseQueue):
    """The ResQ class defines the Redis server object to which we will
    enqueue jobs into various queues.
    """
    client = app.client
    
    @classmethod
    def push(cls, queue, item):
        cls.watch_queue(queue)
        cls.client.rpush("resque:queue:%s" % queue, Message.encode(item))
    
    @classmethod
    def pop(cls, queues, timeout=0):
        if isinstance(queues, basestring):
            queues = [queues]
        ret = cls.client.blpop(["resque:queue:%s" % q for q in queues],
                               timeout=timeout)
        if ret:
            key, ret = ret
            return key[13:], Message.decode(ret)  # trim "resque:queue:"
        else:
            return None, None
    
    @classmethod
    def size(cls, queue):
        return int(cls.client.llen("resque:queue:%s" % queue))
    
    @classmethod
    def watch_queue(cls, queue):
        cls.client.sadd('resque:queues', str(queue))
    
    @classmethod
    def peek(cls, queue, start=0, count=1):
        return cls.list_range('resque:queue:%s' % queue, start, count)
    
    @classmethod
    def list_range(cls, key, start, count):
        items = cls.client.lrange(key, start, start + count - 1) or []
        ret_list = []
        for i in items:
            ret_list.append(Message.decode(i))
        return ret_list
    
    @classmethod
    def queues(cls):
        return cls.client.smembers("resque:queues") or []
    
    @classmethod
    def remove_queue(cls, queue):
        cls.client.srem('resque:queues', queue)
        del cls.client['resque:queue:%s' % queue]
        
    @classmethod
    def keys(cls):
        return [key.replace('resque:', '')
                for key in cls.client.keys('resque:*')]
