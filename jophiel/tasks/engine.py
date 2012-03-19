# -*- coding: utf-8 -*-
"""
Created on 2012-3-9

@author: lzz
"""

import sys
import traceback
import json

from jophiel import signals
from jophiel.utils import ExceptionInfo
from jophiel.tasks import states
from jophiel.app import tasks
from jophiel.backend.taskqueue import TaskQueue

class TraceInfo(object):

    def __init__(self, status=states.PENDING, retval=None, exc_info=None):
        self.status = status
        self.retval = retval
        self.exc_info = exc_info
        self.exc_type = None
        self.exc_value = None
        self.tb = None
        self.strtb = None
        if self.exc_info:
            self.exc_type, self.exc_value, self.tb = exc_info
            self.strtb = "\n".join(traceback.format_exception(*exc_info))

    @classmethod
    def trace(cls, fun, args, kwargs, propagate=False):
        try:
            return cls(states.SUCCESS, retval=fun(*args, **kwargs))
        except Exception, exc:
            if propagate:
                raise
            return cls(states.FAILURE, retval=exc, exc_info=sys.exc_info())
        except BaseException, exc:
            raise
        except:  # pragma: no cover
            # For Python2.5 where raising strings are still allowed
            # (but deprecated)
            if propagate:
                raise
            return cls(states.FAILURE, retval=None, exc_info=sys.exc_info())


class TaskEngine(object):

    def __init__(self, task_name, task_id,queue, args, kwargs, task=None):
        self.task_id = task_id
        self.task_name = task_name
        self.kwargs = kwargs
        self.args = args
        self.queue = queue
        self.task = task or tasks[self.task_name]
        self.status = states.PENDING
        self._trace_handlers = {states.FAILURE: self.handle_failure,
                                states.RETRY: self.handle_retry,
                                states.SUCCESS: self.handle_success}

    def __call__(self):
        return self.execute()

    def execute(self):
        signals.task_prerun.send(sender=self.task, task_id=self.task_id,
                                 task=self.task, kwargs=self.kwargs)
        retval = self._trace()
        signals.task_postrun.send(sender=self.task, task_id=self.task_id,
                                  task=self.task,kwargs=self.kwargs, retval=retval)
        return retval
    
    
    
    def run(self,args,kwargs):
        taskinfo = {
            "task_id":self.task_id,
            "task_name":self.task_name,
            "args":self.args,
            "kwargs":self.kwargs,
            "queue":self.queue
            }
        TaskQueue.enqueue(taskinfo)
       
            
    def _trace(self):
        trace = TraceInfo.trace(self.run,self.args,self.kwargs)
        self.status = trace.status
        self.strtb = trace.strtb
        handler = self._trace_handlers[trace.status]
        r = handler(trace.retval, trace.exc_type, trace.tb, trace.strtb)
        self.handle_after_return(trace.status, trace.retval,
                                 trace.exc_type, trace.tb, trace.strtb,
                                 einfo=trace.exc_info)
        return r

    def handle_after_return(self, status, retval, type_, tb, strtb,
            einfo=None):
        if status == states.EXCEPTION_STATES:
            einfo = ExceptionInfo(einfo)
        self.task.after_return(status, retval, self.task_id,
                               self.args, self.kwargs, einfo)

    
    def handle_success(self, retval, *args):
        """Handle successful execution."""
        self.task.on_success(retval, self.task_id, self.args, self.kwargs)
        return retval

    def handle_retry(self, exc, type_, tb, strtb):
        """Handle retry exception."""
        message, orig_exc = exc.args
        expanded_msg = "%s: %s" % (message, str(orig_exc))
        einfo = ExceptionInfo((type_, type_(expanded_msg, None), tb))
        self.task.on_retry(exc, self.task_id, self.args, self.kwargs, einfo)
        return einfo

    def handle_failure(self, exc, type_, tb, strtb):
        """Handle exception."""
        einfo = ExceptionInfo((type_, exc, tb))
        self.task.on_failure(exc, self.task_id, self.args, self.kwargs, einfo)
        signals.task_failure.send(sender=self.task, task_id=self.task_id,
                                  exception=exc, args=self.args,
                                  kwargs=self.kwargs, traceback=tb,
                                  einfo=einfo)
        return einfo
