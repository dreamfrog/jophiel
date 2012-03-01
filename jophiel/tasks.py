'''
Created on 2012-2-29

@author: lzz
'''

import threading
import sys
import inspect
import uuid

from .errors import NoRegisterError
from .utils import fun_takes_kwargs
from .trace import TaskTrace
from .utils import ExceptionInfo


class TaskRegistry(dict):

    def register(self, task):
        """
        Register a task in the task registry.
        """
        self[task.name] = inspect.isclass(task) and task() or task

    def unregister(self, name):
        try:
            name = name.name
        except AttributeError:
            pass
        self.pop(name)

    def filter_types(self, type):
        """Return all tasks of a specific type."""
        return dict((name, task) for name, task in self.iteritems()
                                    if task.type == type)

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError:
            raise NoRegisterError

    def pop(self, key, *args):
        try:
            return dict.pop(self, key, *args)
        except KeyError:
            raise NoRegisterError


#: Global task registry.
tasks = TaskRegistry()


class Context(threading.local):
    id = None
    args = None
    kwargs = None
    retries = 0

    def update(self, d, **kwargs):
        self.__dict__.update(d, **kwargs)

    def clear(self):
        self.__dict__.clear()

    def get(self, key, default=None):
        try:
            return getattr(self, key)
        except AttributeError:
            return default


class TaskType(type):

    def __new__(cls, name, bases, attrs):
        new = super(TaskType, cls).__new__
        task_module = attrs.get("__module__") or "__main__"

        # Abstract class: abstract attribute should not be inherited.
        if attrs.pop("abstract", None) or not attrs.get("autoregister", True):
            return new(cls, name, bases, attrs)

        # Automatically generate missing/empty name.
        autoname = False
        if not attrs.get("name"):
            try:
                module_name = sys.modules[task_module].__name__
            except KeyError:  # pragma: no cover
                # Fix for manage.py shell_plus (Issue #366).
                module_name = task_module
            attrs["name"] = '.'.join([module_name, name])
            autoname = True

        task_name = attrs["name"]
        if task_name not in tasks:
            task_cls = new(cls, name, bases, attrs)
            tasks.register(task_cls)
        task = tasks[task_name].__class__


        return task


class BaseTask(object):
    """Task base class.
    """
    __metaclass__ = TaskType

    abstract = True
    
    name = None
    queue = None
    
    request = Context()
        
    max_retries = 3
    ignore_result = False
    result_backend = None

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


    def run(self, *args, **kwargs):
        raise NotImplementedError("Tasks must define the run method.")

    @classmethod
    def apply(self, args=None, kwargs=None, **options):
        """Execute this task locally, by blocking until the task returns.
        """
        args = args or []
        kwargs = kwargs or {}
        task_id = options.get("task_id") or uuid.uuid4().hex
        retries = options.get("retries", 0)

        # Make sure we get the task instance, not class.
        task = tasks[self.name]

        request = {"id": task_id,
                   'name':self.name,
                   "retries": retries,
                   }
        
        default_kwargs = {"task_name": task.name,
                          "task_id": task_id,
                          "task_retries": retries,
                          }
        
        supported_keys = fun_takes_kwargs(task.run, default_kwargs)
        extend_with = dict((key, val)
                                for key, val in default_kwargs.items()
                                    if key in supported_keys)
        kwargs.update(extend_with)


        trace = TaskTrace(task.name, task_id, args, kwargs,
                          task=task, request=request)
        retval = trace.execute()
        if isinstance(retval, ExceptionInfo):
            retval = retval.exception
        return EagerResult(task_id, retval, trace.status,
                           traceback=trace.strtb)

    @classmethod
    def AsyncResult(self, task_id):
        """Get AsyncResult instance for this kind of task.

        :param task_id: Task id to get result for.

        """
        return self.app.AsyncResult(task_id, backend=self.backend,
                                             task_name=self.name)

    def update_state(self, task_id=None, state=None, meta=None):
        """Update task state.

        :param task_id: Id of the task to update.
        :param state: New state (:class:`str`).
        :param meta: State metadata (:class:`dict`).

        """
        if task_id is None:
            task_id = self.request.id
        self.backend.store_result(task_id, meta, state)

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        """Retry handler."""
        pass

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

    def send_error_email(self, context, exc, **kwargs):
        if self.send_error_emails and not self.disable_error_emails:
            sender = self.ErrorMail(self, **kwargs)
            sender.send(context, exc)

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def execute(self, request, **kwargs):
        pass

    def __repr__(self):
        """`repr(task)`"""
        return "<@task: %s>" % (self.name, )


    @property
    def __name__(self):
        return self.__class__.__name__
    

from utils import safe_str_to_class
import failure

from datetime import timedelta

class Job(object):
    
    safe_str_to_class = staticmethod(safe_str_to_class)
    
    def __init__(self, queue, payload, resq, worker=None):
        self._queue = queue
        self._payload = payload
        self.resq = resq
        self._worker = worker

    def __str__(self):
        return "(Job{%s} | %s | %s)" % (
            self._queue, self._payload['class'], repr(self._payload['args']))

    def perform(self):
        """
        #@ add entry_point loading
        """
        payload_class_str = self._payload["class"]
        payload_class = self.safe_str_to_class(payload_class_str)
        payload_class.resq = self.resq
        args = self._payload.get("args")

        try:
            return payload_class.perform(*args)
        except:
            if not self.retry(payload_class, args):
                raise

    def fail(self, exception):
        """This method provides a way to fail a job and will use whatever
        failure backend you've provided. The default is the ``RedisBackend``.
        """
        fail = failure.create(exception, self._queue, self._payload,
                              self._worker)
        fail.save(self.resq)
        return fail

    def retry(self, payload_class, args):
        retry_every = getattr(payload_class, 'retry_every', None)
        retry_timeout = getattr(payload_class, 'retry_timeout', 0)

        if retry_every:
            now = self.resq._current_time()
            first_attempt = self._payload.get("first_attempt", now)
            retry_until = first_attempt + timedelta(seconds=retry_timeout)
            retry_at = now + timedelta(seconds=retry_every)
            if retry_at < retry_until:
                self.resq.enqueue_at(retry_at, payload_class, *args,
                        **{'first_attempt':first_attempt})
                return True
        return False

    @classmethod
    def reserve(cls, queues, res, worker=None, timeout=10):
        """Reserve a job on one of the queues. This marks this job so
        that other workers will not pick it up.
        """
        if isinstance(queues, basestring):
            queues = [queues]
        queue, payload = res.pop(queues, timeout=timeout)
        if payload:
            return cls(queue, payload, res, worker)   
