#encoding=utf-8
'''
Created on 2012-3-9

@author: lzz
'''
import sys

"""
    generate default name for task and other attribute to task
"""
class TaskDescriptor(type):
    def __new__(cls, name, bases, attrs):
        new = super(TaskDescriptor, cls).__new__
        task_module = attrs.get("__module__") or "__main__"
        if not attrs.get("name"):
            try:
                module_name = sys.modules[task_module].__name__
            except KeyError:  
                module_name = task_module
            attrs["name"] = '.'.join([module_name, name])
        task_cls = new(cls, name, bases, attrs)
        return task_cls

"""Task base class.
"""   
class Task(object):
    
    __metaclass__ = TaskDescriptor
        
    def __init__(self,task_id,*args,**kwargs):
        self.task_id = task_id
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        """`repr(task)`"""
        return "<@task: %s,%s>" % (self.name,self.task_id )
     
    def run(self, *args, **kwargs):
        raise NotImplementedError("Tasks must define the run method.")
    
    """hook for task processing"""
    def after_return(self, status, retval, einfo):pass
    def on_success(self, retval, task_id, *args, **kwargs):pass
    def on_failure(self, retval, task_id, einfo,*args, **kwargs):pass  
    def on_retry(self,retval,task_id,einfo,*args,**kwargs):pass