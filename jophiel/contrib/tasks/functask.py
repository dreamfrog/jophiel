'''
Created on 2012-3-30

@author: lzz
'''
from jophiel.tasks.base import Task
import importlib

class FuncTask(Task):
    
    @property
    def func_name(self):
        return self._func_name

    @property
    def func(self):
        func_name = self.func_name
        if func_name is None:
            return None

        module_name, func_name = func_name.rsplit('.', 1)
        module = importlib.import_module(module_name)
        return getattr(module, func_name)