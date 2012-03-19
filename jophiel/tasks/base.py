'''
Created on 2012-3-9

@author: lzz
'''
import sys

class TaskMeta(type):

    def __new__(cls, name, bases, attrs):
        new = super(TaskMeta, cls).__new__
        task_module = attrs.get("__module__") or "__main__"

        # Automatically generate missing/empty name.
        if not attrs.get("name"):
            try:
                module_name = sys.modules[task_module].__name__
            except KeyError:  # pragma: no cover
                # Fix for manage.py shell_plus (Issue #366).
                module_name = task_module
            attrs["name"] = '.'.join([module_name, name])
        
        task_cls = new(cls, name, bases, attrs)
        return task_cls


class  Task(object):
    """Task base class.
    """
    __metaclass__ = TaskMeta
    
    name = None 
    
    def __init__(self,task_id,args,kwargs):
        self.task_id = task_id
        self.args = args
        self.kwargs = kwargs
    
    def perform(self):
        self.run(*self.args,**self.kwargs)
    
    @classmethod
    def run(cls, *args, **kwargs):
        raise NotImplementedError("Tasks must define the run method.")
    
    @classmethod
    def after_return(cls, status, retval, task_id, args, kwargs, einfo):
        pass

    """hook for task processing"""
    @classmethod
    def on_success(cls, retval, task_id, args, kwargs):
        pass
    @classmethod
    def on_retry(cls, exc, task_id, args, kwargs, einfo):
        """Retry handler."""
        pass
    @classmethod
    def on_failure(cls, exc, task_id, args, kwargs, einfo):
        pass
    
    def __repr__(self):
        """`repr(task)`"""
        return "<@task: %s>" % (self.name, )

    @property
    def __name__(self):
        return self.__class__.__name__
    
    