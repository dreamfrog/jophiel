'''
Created on 2012-2-23

@author: lzz
'''

from redis import Redis
from log import logger
import time
import datetime

from jophiel.utils import json_parser as json
import redisclient 

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

class TaskQueue(object):pass

class RedisQueue(object):
    """The ResQ class defines the Redis server object to which we will
    enqueue jobs into various queues.
    """
    def __init__(self,):
        self.redis = redisclient.client

    def push(self, queue, item):
        self.watch_queue(queue)
        self.redis.rpush("resque:queue:%s" % queue, TaskMessage.encode(item))

    def pop(self, queues, timeout=10):
        if isinstance(queues, basestring):
            queues = [queues]
        ret = self.redis.blpop(["resque:queue:%s" % q for q in queues],
                               timeout=timeout)
        if ret:
            key, ret = ret
            return key[13:], TaskMessage.decode(ret)  # trim "resque:queue:"
        else:
            return None, None

    def size(self, queue):
        return int(self.redis.llen("resque:queue:%s" % queue))

    def watch_queue(self, queue):
        self.redis.sadd('resque:queues', str(queue))

    def peek(self, queue, start=0, count=1):
        return self.list_range('resque:queue:%s' % queue, start, count)

    def list_range(self, key, start, count):
        items = self.redis.lrange(key, start, start + count - 1) or []
        ret_list = []
        for i in items:
            ret_list.append(TaskMessage.decode(i))
        return ret_list

    def enqueue(self, klass, *args):
        
        queue = getattr(klass, 'queue', None)
        if queue:
            class_name = '%s.%s' % (klass.__module__, klass.__name__)
            self.push(queue, {'class':class_name, 'args':args})
            logger.info("enqueued '%s' job on queue %s" % (class_name, queue))
            if args:
                logger.debug("job arguments: %s" % str(args))
            else:
                logger.debug("no arguments passed in.")
        else:
            logger.warning("unable to enqueue job with class %s" % str(klass))

    def enqueue_from_string(self, klass_as_string, queue, *args, **kwargs):
        payload = {'class':klass_as_string, 'queue': queue, 'args':args}
        if 'first_attempt' in kwargs:
            payload['first_attempt'] = kwargs['first_attempt']
        self.push(queue, payload)
        logger.info("enqueued '%s' job on queue %s" % (klass_as_string, queue))
        if args:
            logger.debug("job arguments: %s" % str(args))
        else:
            logger.debug("no arguments passed in.")

    def queues(self):
        return self.redis.smembers("resque:queues") or []


    def keys(self):
        return [key.replace('resque:', '')
                for key in self.redis.keys('resque:*')]

    def remove_queue(self, queue):
        self.redis.srem('resque:queues', queue)
        del self.redis['resque:queue:%s' % queue]

    def enqueue_at(self, datetime, klass, *args, **kwargs):
        class_name = '%s.%s' % (klass.__module__, klass.__name__)
        logger.info("scheduled '%s' job on queue %s for execution at %s" % 
                     (class_name, klass.queue, datetime))
        if args:
            logger.debug("job arguments are: %s" % str(args))
        payload = {'class':class_name, 'queue': klass.queue, 'args':args}
        if 'first_attempt' in kwargs:
            payload['first_attempt'] = kwargs['first_attempt']
        self.delayed_push(datetime, payload)

    def delayed_push(self, datetime, item):
        key = int(time.mktime(datetime.timetuple()))
        self.redis.rpush('resque:delayed:%s' % key, TaskMessage.encode(item))
        self.redis.zadd('resque:delayed_queue_schedule', key, key)

    def delayed_queue_peek(self, start, count):
        return [int(item) for item in self.redis.zrange(
                'resque:delayed_queue_schedule', start, start + count) or []]

    def delayed_timestamp_peek(self, timestamp, start, count):
        return self.list_range('resque:delayed:%s' % timestamp, start, count)

    def delayed_queue_schedule_size(self):
        size = 0
        length = self.redis.zcard('resque:delayed_queue_schedule')
        for i in self.redis.zrange('resque:delayed_queue_schedule', 0, length):
            size += self.delayed_timestamp_size(i)
        return size

    def delayed_timestamp_size(self, timestamp):
        #key = int(time.mktime(timestamp.timetuple()))
        return self.redis.llen("resque:delayed:%s" % timestamp)

    def next_delayed_timestamp(self):
        key = int(time.mktime(self._current_time().timetuple()))
        array = self.redis.zrangebyscore('resque:delayed_queue_schedule',
                                         '-inf', key)
        timestamp = None
        if array:
            timestamp = array[0]
        return timestamp

    def next_item_for_timestamp(self, timestamp):
        #key = int(time.mktime(timestamp.timetuple()))
        key = "resque:delayed:%s" % timestamp
        ret = self.redis.lpop(key)
        item = None
        if ret:
            item = TaskMessage.decode(ret)
        if self.redis.llen(key) == 0:
            self.redis.delete(key)
            self.redis.zrem('resque:delayed_queue_schedule', timestamp)
        return item

    @classmethod
    def _enqueue(cls, klass, *args):
        queue = getattr(klass, 'queue', None)
        _self = cls()
        if queue:
            class_name = '%s.%s' % (klass.__module__, klass.__name__)
            _self.push(queue, {'class':class_name, 'args':args})

    @staticmethod
    def _current_time():
        return datetime.datetime.now()

