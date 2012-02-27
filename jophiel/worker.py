import logging
import signal
import datetime, time
import os, sys
import commands
import random

from jophiel.utils import json_parser as json
from jophiel.exceptions import NoQueueError
from jophiel.jobs import Job
from jophiel.taskqueue import RedisQueue
from jophiel.resource import Stat

from jophiel import __version__
from jophiel.utils import setproctitle
from jophiel.redisclient import client
from jophiel.resource import WorkerResource

logger = logging.getLogger(__name__)

class BasicWorker(object):
    
    def __init__(self,queues,job_class,*args,**argv):
        self.child = None
        self._shutdown = False
        
        self.job_class = job_class
        self.worker = WorkerResource()
        self.queues = queues
        self.resq = RedisQueue()
        self.redis = client
        
        self.validate_queues()
        
    def shutdown_all(self, signum, frame):
        self.schedule_shutdown(signum, frame)
        self.kill_child(signum, frame)

    def schedule_shutdown(self, signum, frame):
        self._shutdown = True

    def kill_child(self, signum, frame):
        if self.child:
            logger.info("Killing child at %s" % self.child)
            os.kill(self.child, signal.SIGKILL)

    def register_signal_handlers(self):
        signal.signal(signal.SIGTERM, self.shutdown_all)
        signal.signal(signal.SIGINT, self.shutdown_all)
        signal.signal(signal.SIGQUIT, self.schedule_shutdown)
        signal.signal(signal.SIGUSR1, self.kill_child)

    def worker_pids(self):
        """Returns an array of all pids (as strings) of the workers on
        this machine.  Used when pruning dead workers."""
        return map(lambda l: l.strip().split(' ')[0],
                   commands.getoutput("ps -A -o pid,command | \
                                       grep pyres_worker").split("\n"))


    def validate_queues(self):
        """Checks if a worker is given at least one queue to work on."""
        if not self.queues:
            raise NoQueueError("Please give each worker at least one queue.")

    def startup(self):
        self.register_signal_handlers()
        self.worker.prune_dead_workers(self.worker_pids())
        self.worker.register_worker()

    def stop(self):
        self.worker.unregister_worker()

    def before_fork(self, job):
        pass

    def after_fork(self, job):
        pass

    def before_process(self, job):
        return job

    def process(self, job=None):
        if not job:
            job = self.reserve()
        try:
            self.worker.working_on(job)
            job = self.before_process(job)
            return job.perform()
        except Exception, e:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            logger.exception("%s failed: %s" % (job, e))
            job.fail(exceptionTraceback)
            self.worker.failed()
        else:
            logger.info('completed job')
            logger.debug('job details: %s' % job)
        finally:
            self.worker.done_working()

    def reserve(self, timeout=10):
        logger.debug('checking queues %s' % self.queues)
        job = self.job_class.reserve(self.queues, self.__str__(), timeout=timeout)
        if job:
            logger.info('Found job on %s' % job._queue)
            return job

                
class Worker(BasicWorker):
    """Defines a worker. The ``pyres_worker`` script instantiates this Worker
    class and passes a comma-separated list of queues to listen on.::

       >>> from pyres.worker import Worker
       >>> Worker.run([queue1, queue2], server="localhost:6379")

    """
    
    job_class = Job
    
    def __init__(self, queues=()):
        super(Worker,self).__init__(queues,self.job_class)

    def _setproctitle(self, msg):
        setproctitle("pyres_worker-%s [%s]: %s" % (__version__,
                                                   ','.join(self.queues),
                                                   msg))

    def work(self, interval=5):
        """Invoked by ``run`` method. ``work`` listens on a list of queues and sleeps
        for ``interval`` time
        ``interval`` -- Number of seconds the worker will wait until processing the next job. 
            Default is "5".
        """
        self._setproctitle("Starting")

        while True:
            if self._shutdown:
                logger.info('shutdown scheduled')
                break

            job = self.reserve(interval)

            if job:
                logger.debug('picked up job')
                logger.debug('job details: %s' % job)
                self.before_fork(job)
                self.child = os.fork() 
                if self.child:
                    self._setproctitle("Forked %s at %s" % 
                                       (self.child,datetime.datetime.now()))
                    logger.info('Forked %s at %s' % 
                                (self.child,datetime.datetime.now()))

                    try:
                        os.waitpid(self.child, 0)
                    except OSError as ose:
                        import errno

                        if ose.errno != errno.EINTR:
                            raise ose
                    #os.wait()
                    logger.debug('done waiting')
                else:
                    self._setproctitle("Processing %s since %s" % 
                                       (job._queue,datetime.datetime.now()))
                    logger.info('Processing %s since %s' % 
                                 (job._queue, datetime.datetime.now()))
                    self.after_fork(job)

                    # re-seed the Python PRNG after forking, otherwise
                    # all job process will share the same sequence of
                    # random numbers
                    random.seed()

                    self.process(job)
                    os._exit(0)
                self.child = None
            else:
                if interval == 0:
                    break
                #procline @paused ? "Paused" : "Waiting for #{@queues.join(',')}"
                self._setproctitle("Waiting")
                #time.sleep(interval)
        self.stop


    @classmethod
    def run(cls, queues, interval=None):
        worker = cls(queues=queues)
        worker.startup()
        
        if interval is not None:
            worker.work(interval)
        else:
            worker.work()
            

if __name__ == "__main__":
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-q", dest="queue_list")
    parser.add_option("-s", dest="server", default="localhost:6379")
    (options, args) = parser.parse_args()
    if not options.queue_list:
        parser.print_help()
        parser.error("Please give each worker at least one queue.")
    queues = options.queue_list.split(',')
    Worker.run(queues, options.server)
