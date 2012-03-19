'''
Created on 2012-3-12

@author: lzz
'''

import time
import datetime

from jophiel.backend.base import BaseQueue
from jophiel.backend.base import TaskMessage
from jophiel import app
from jophiel.app import logger

class BasicMessageQueue(BaseQueue):
    """The ResQ class defines the Redis server object to which we will
    enqueue jobs into various queues.
    """
    client = app.client
    
    @classmethod
    def push(cls, queue, item):
        cls.watch_queue(queue)
        cls.client.rpush("resque:queue:%s" % queue, TaskMessage.encode(item))
    
    @classmethod
    def pop(cls, queues, timeout=0):
        if isinstance(queues, basestring):
            queues = [queues]
        ret = cls.client.blpop(["resque:queue:%s" % q for q in queues],
                               timeout=timeout)
        if ret:
            key, ret = ret
            return key[13:], TaskMessage.decode(ret)  # trim "resque:queue:"
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
            ret_list.append(TaskMessage.decode(i))
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

 
class TimeRedisQueue(BasicMessageQueue): 
    
    @classmethod
    def delayed_push(cls, datetime, item):
        key = int(time.mktime(datetime.timetuple()))
        cls.client.rpush('resque:delayed:%s' % key, TaskMessage.encode(item))
        cls.client.zadd('resque:delayed_queue_schedule', key, key)
    
    @classmethod
    def delayed_queue_peek(cls, start, count):
        return [int(item) for item in cls.client.zrange(
                'resque:delayed_queue_schedule', start, start + count) or []]
    @classmethod
    def delayed_timestamp_peek(cls, timestamp, start, count):
        return cls.list_range('resque:delayed:%s' % timestamp, start, count)

    @classmethod
    def delayed_queue_schedule_size(cls):
        size = 0
        length = cls.client.zcard('resque:delayed_queue_schedule')
        for i in cls.client.zrange('resque:delayed_queue_schedule', 0, length):
            size += cls.delayed_timestamp_size(i)
        return size
    
    @classmethod
    def delayed_timestamp_size(cls, timestamp):
        #key = int(time.mktime(timestamp.timetuple()))
        return cls.client.llen("resque:delayed:%s" % timestamp)

    @classmethod
    def next_delayed_timestamp(cls):
        key = int(time.mktime(cls._current_time().timetuple()))
        array = cls.client.zrangebyscore('resque:delayed_queue_schedule',
                                         '-inf', key)
        timestamp = None
        if array:
            timestamp = array[0]
        return timestamp
    
    @classmethod
    def next_item_for_timestamp(cls, timestamp):
        #key = int(time.mktime(timestamp.timetuple()))
        key = "resque:delayed:%s" % timestamp
        ret = cls.client.lpop(key)
        item = None
        if ret:
            item = TaskMessage.decode(ret)
        if cls.client.llen(key) == 0:
            cls.client.delete(key)
            cls.client.zrem('resque:delayed_queue_schedule', timestamp)
        return item

    @staticmethod
    def _current_time():
        return datetime.datetime.now()
