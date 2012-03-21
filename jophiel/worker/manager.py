'''
Created on 2012-3-9

@author: lzz
'''

import signal

import os
import multiprocessing
import time 
import threading

from jophiel import app
from jophiel.app import client
from jophiel.worker import node
from jophiel.worker.base import Worker

logger = app.logger

"""
    work manager,response for processing system signals,mulsti tasks etc.
"""
class Manager(object):
    def __init__(self, queue, host,port,internal = 60):
        self.queue = queue
        self.running = False
        self.workers =None
        self.server = node.ServerThread(self.host,self.port)
        self.internal = internal
        self.monitor = threading.Thread(target=self.beatheat)
        self.worker = Worker(self.queue)
    
    def beatheat(self):
        while not self.running:
            'send some beatheat messages'
            "print send meaage"
            print "beat,",time.time()
            time.sleep(self.internal)
            
    def startup(self):
        self.running = True
        self.server.start()
        self.monitor.start()
        self.register_signals()
    
    def stop(self):pass

    def work(self):
        self.startup()
        self.worker.start()

    def register_signals(self):
        signal.signal(signal.SIGTERM, self.shutdown_all)
        signal.signal(signal.SIGINT, self.shutdown_all)

    def shutdown_all(self, signum, frame):
        self.schedule_shutdown(signum, frame)
        
    def schedule_shutdown(self, signum, frame):
        self.running = False
        self.worker.schedule_down()
        
    @classmethod
    def run(cls, queue):
        manager = cls(queue)
        manager.work()

    def __str__(self):
        hostname = os.uname()[1]
        pid = os.getpid()
        return '%s:%s:%s' % (hostname, pid, ','.join(self.queue))
        
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
