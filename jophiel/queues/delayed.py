'''
Created on 2012-3-23

@author: lzz
'''


import time
import datetime

from .message import Message
from .base import BaseQueue
from .message import MessageQueue

class TimeRedisQueue(MessageQueue): 
    
    @classmethod
    def delayed_push(cls, datetime, item):
        key = int(time.mktime(datetime.timetuple()))
        cls.client.rpush('resque:delayed:%s' % key, Message.encode(item))
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
            item = Message.decode(ret)
        if cls.client.llen(key) == 0:
            cls.client.delete(key)
            cls.client.zrem('resque:delayed_queue_schedule', timestamp)
        return item

    @staticmethod
    def _current_time():
        return datetime.datetime.now()