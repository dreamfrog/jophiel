'''
Created on 2012-3-1

@author: lzz
'''
import datetime
import os

from jophiel.worker.base import BasicWorker
from jophiel.app import logger


logger = logger
           
class Worker(BasicWorker):
    """
    Defines a worker.
    """
    def __init__(self, queues=()):
        super(Worker,self).__init__(queues)
        self._shutdown = False
        
    def shutdown_all(self, signum, frame):
        self._shutdown = True

    def before_fork(self, job):
        pass

    def after_fork(self, job):
        pass
    
    def work(self):
        while True:
            if self._shutdown:
                logger.info('shutdown scheduled')
                break

            task = self.next_task()
            self.child = None
            if task:
                logger.debug('picked up job,job details: %s' % task)
                self.before_fork(task)
                self.child = os.fork() 
                if self.child:
                    logger.info('Forked %s at %s' % (self.child,datetime.datetime.now()))
                    
                    try:
                        os.waitpid(self.child, 0)
                    except OSError as ose:
                        """???need to consider the system interrupt condition
                        """
                        import errno
                        if ose.errno != errno.EINTR:
                            raise ose
                    logger.debug('done waiting')
                else:
                    logger.info('Processing %s since %s' % (task._queue, datetime.datetime.now()))
                    self.after_fork(task)
                    self.process(task)
                    os._exit(0)


if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-q", dest="queue_name")
    (options, args) = parser.parse_args()
    if not options.queue_name:
        parser.print_help()
        parser.error("Please give each worker at least one queue.")
    queue = options.queue_name
    Worker.run(queue)
