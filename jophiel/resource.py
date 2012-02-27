'''
Created on 2012-2-25

@author: lzz
'''
import os
import time
import datetime
import logging
import json

from jophiel.redisclient import client
from jophiel.taskqueue import TaskMessage

logger = logging.getLogger(__name__)

class Stat(object):
    """A Stat class which shows the current status of the queue.

    """
    def __init__(self, name):
        self.name = name
        self.key = "resque:stat:%s" % self.name
        self.redis = client

    def get(self):
        val = self.redis.get(self.key)
        if val:
            return int(val)
        return 0

    def incr(self, ammount=1):
        self.redis.incr(self.key, ammount)

    def decr(self, ammount=1):
        self.redis.decr(self.key, ammount)

    def clear(self):
        self.redis.delete(self.key)
        

class WorkerResource(object):
    
    redis = client
    
    def __init__(self,queues,worker_id = None):
        self.worker_id =worker_id
        self.queues = queues
        self.pid = os.getpid()
        self.hostname = os.uname()[1]

    def __str__(self):
        if self.worker_id:
            return self.worker_id
        return '%s:%s:%s' % (self.hostname, self.pid, ','.join(self.queues))
    
    @classmethod
    def all(cls):

        return [cls.find(w) for w in cls.redis.smembers('resque:workers') or []]

    @classmethod
    def working(cls, host):
        redis = client
        total = []
        for key in cls.all():
            total.append('resque:worker:%s' % key)
        names = []
        for key in total:
            value = redis.get(key)
            if value:
                w = cls.find(key[14:]) #resque:worker:
                names.append(w)
        return names

    @classmethod
    def find(cls, worker_id):
        if cls.exists(worker_id):
            queues = worker_id.split(':')[-1].split(',')
            worker = cls(queues)
            worker.id = worker_id
            return worker
        else:
            return None

    @classmethod
    def exists(cls, worker_id):
        return cls.redis.sismember('resque:workers', worker_id)
    
    @classmethod
    def get_processed(cls,worker_id):
        return Stat("processed:%s"%worker_id ).get()

    def processed(self):
        return Stat("processed:%s"%self ).get()

    def process(self):
        total_processed = Stat("processed")
        worker_processed = Stat("processed:%s" % str(self))
        total_processed.incr()
        worker_processed.incr()

    
    def fail(self):
        Stat("failed").incr()
        Stat("failed:%s" % self).incr()

    @classmethod
    def get_failed(cls,worker_id):
        return Stat("failed:%s" % worker_id).get()
    
    def failed(self):
        Stat("failed:%s"%self).get()
        

    def job(self):
        data = self.redis.get("resque:worker:%s" % self)
        if data:
            return json.loads(data)
        return {}


    def _set_started(self, dt):
        if dt:
            key = int(time.mktime(dt.timetuple()))
            self.redis.set("resque:worker:%s:started" % self, key)
        else:
            self.redis.delete("resque:worker:%s:started" % self)

    def _get_started(self):
        datestring = self.redis.get("resque:worker:%s:started" % self)
        #ds = None
        #if datestring:
        #    ds = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M:%S')
        return datestring

    started = property(_get_started, _set_started)

    def register_worker(self):
        self.redis.sadd('resque:workers', str(self))
        #self.resq._redis.add("worker:#{self}:started", Time.now.to_s)
        self.started = datetime.datetime.now()
        
    def unregister_worker(self):
        self.redis.srem('resque:workers', str(self))
        self.started = None
        Stat("processed:%s" % self).clear()
        Stat("failed:%s" % self ).clear()

    def prune_dead_workers(self,worker_pids):
        all_workers = self.all()
        known_workers = worker_pids
        for worker in all_workers:
            host, pid, queues = worker.id.split(':')
            if host != self.hostname:
                continue
            if pid in known_workers:
                continue
            worker.unregister_worker()

    def working_on(self, job):
        logger.debug('marking as working on')
        data = {
            'queue': job._queue,
            'run_at': str(int(time.mktime(datetime.datetime.now().timetuple()))),
            'payload': job._payload
        }
        data = json.dumps(data)
        self.redis["resque:worker:%s" % str(self)] = data
        logger.debug("worker:%s" % str(self))
        logger.debug(self.redis["resque:worker:%s" % str(self)])

    def done_working(self):
        logger.info('done working')
        self.processed()
        self.redis.delete("resque:worker:%s" % str(self))

    def processing(self):
        return self.job()

    def state(self):
        if self.redis.exists('resque:worker:%s' % self):
            return 'working'
        return 'idle'



class AllResource(object):
    def __init__(self,taskqueue,workers):
        self.taskqueue = taskqueue
    def info(self):
        """Returns a dictionary of the current status of the pending jobs,
        processed, no. of queues, no. of workers, no. of failed jobs.

        """
        pending = 0
        for q in self.taskqueue.queues():
            pending += self.taskqueue.size(q)
        return {
            'pending'   : pending,
            'processed' : Stat('processed', self).get(),
            'queues'    : len(self.taskqueue.queues()),
            #'workers'   : len(self.workers()),
            #'working'   : len(self.working()),
            'failed'    : Stat('failed', self).get(),
            #'servers'   : ['%s:%s' % (self.host, self.port)]
        }   
