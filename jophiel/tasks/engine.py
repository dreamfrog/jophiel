# -*- coding: utf-8 -*-
"""
Created on 2012-3-9

@author: lzz
"""
import sys
import traceback

from jophiel import signals
from jophiel.utils import ExceptionInfo
from jophiel.tasks import states
from jophiel.app import tasks
from jophiel.tasks.utils import build_task

def processsing(func):
    def new_func(self,*args, **kwargs):
        signals.task_prerun.send(sender=self.task)
        retval = func(self,*args,**kwargs)
        signals.task_postrun.send(sender=self.task,retval=retval)
        return retval
    return new_func 
             
class TaskTrace(object):

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
    def trace(cls, fun, propagate=False,*args, **kwargs):
        try:
            retval=fun(*args, **kwargs)
            return cls(states.SUCCESS,retval)
        except Exception, exc:
            if propagate:
                raise
            return cls(states.FAILURE, retval=exc, exc_info=sys.exc_info())
        except BaseException, exc:
            raise

class ExecuteEngine(object):

    def __init__(self,task,*args, **kwargs):
        self.task_id = task.task_id
        self.task_name = task.task_name
        self.args = args
        self.kwargs = kwargs
        self.task = task(self.task_id) or tasks[self.task_name](self.task_id)
        self.status = states.PENDING
        self._trace_handlers = {
                                states.FAILURE: self.handle_failure,
                                states.RETRY: self.handle_retry,
                                states.SUCCESS: self.handle_success
                                }

    @processsing
    def execute(self):
        trace = TaskTrace.trace(self.task.run,*self.args,**self.kwargs)
        self.status = trace.status
        self.strtb = trace.strtb
        
        handler = self._trace_handlers[trace.status]
        r = handler(trace.retval, trace.exc_type, trace.tb, trace.strtb)
        self.handle_after_return(trace.status, trace.retval,
                         trace.exc_type, trace.tb, trace.strtb,
                         einfo=trace.exc_info)
        return r
    
    @classmethod
    def run(self,taskinfo):
        task = build_task(taskinfo)
        engine = ExecuteEngine(task)
        engine.execute(task,*task.args,**task.kwargs)
        return engine     
    
    def handle_after_return(self, status, retval, type_, tb, strtb,
            einfo=None):
        if status == states.EXCEPTION_STATES:
            einfo = ExceptionInfo(einfo)
        self.task.after_return(status, retval, einfo)

    """Handle successful execution."""
    def handle_success(self, retval, *args):

        self.task.on_success(retval, self.task_id, self.args, self.kwargs)
        return retval
    
    """Handle retry exception."""
    def handle_retry(self, exc, type_, tb, strtb):

        message, orig_exc = exc.args
        expanded_msg = "%s: %s" % (message, str(orig_exc))
        einfo = ExceptionInfo((type_, type_(expanded_msg, None), tb))
        self.task.on_retry(exc, self.task_id, self.args, self.kwargs, einfo)
        return einfo
    
    """Handle exception."""
    def handle_failure(self, exc, type_, tb, strtb):

        einfo = ExceptionInfo((type_, exc, tb))
        self.task.on_failure(exc, self.task_id, self.args, self.kwargs, einfo)
        signals.task_failure.send(sender=self.task, task_id=self.task_id,
                                  exception=exc, args=self.args,
                                  kwargs=self.kwargs, traceback=tb,
                                  einfo=einfo)
        return einfo

def perform(taskinfo):
    ExecuteEngine.execute(taskinfo)