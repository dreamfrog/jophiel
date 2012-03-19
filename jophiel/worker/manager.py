'''
Created on 2012-3-9

@author: lzz
'''

import signal

import os
import multiprocessing

from jophiel import app
from jophiel.app import client
from jophiel.worker.worker import Worker

logger = app.logger

"""
    work manager,response for process system signals,mulsti tasks etc.
"""
class Manager(object):
    def __init__(self, queues, host, max_children=10):
        self.queues = queues
        self._shutdown = False
        self.redis = client
        self.workers = []
        self.children = []

    def __str__(self):
        hostname = os.uname()[1]
        pid = os.getpid()
        return 'manager:%s:%s:%s' % (hostname, pid, ','.join(self.queues))

    """???remove the dependence
    """
    def register_manager(self):
        self.redis.sadd('resque:managers', str(self))

    def unregister_manager(self):
        self.redis.srem('resque:managers', str(self))
            
    def startup(self):
        self.register_manager()
        self.register_signals()
    
    def stop(self):
        self.unregister_manager()
    """
    ???need to enhance functions,exit,quit,children manager etc
    """
    def work(self):
        self.startup()
        #check to see if stuff is still going
        for queue in self.queues:
            self.start_child(queue)
        for child in self.children:
            child.join()

    def register_signals(self):
        signal.signal(signal.SIGTERM, self.shutdown_all)
        signal.signal(signal.SIGINT, self.shutdown_all)
        signal.signal(signal.SIGUSR1, self.kill_children)

    def shutdown_all(self, signum, frame):
        self.schedule_shutdown(signum, frame)
        self.kill_children()

    def schedule_shutdown(self, signum, frame):
        self._shutdown = True

    def kill_children(self):
        for child in self.children:
            child.terminate()

    def start_child(self, queue):
        p = multiprocessing.Process(target=Worker.run, args=(queue,))
        self.children.append(p)
        p.start()

    @classmethod
    def run(cls, queues=()):
        manager = cls(queues)
        manager.work()
        
if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-q", dest="queue_list")
    (options, args) = parser.parse_args()
    if not options.queue_list:
        parser.print_help()
        parser.error("Please give each worker at least one queue.")
    queues = options.queue_list.split()
    Manager.run(queues)
