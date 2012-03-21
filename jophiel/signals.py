'''
Created on 2012-2-29

@author: lzz
'''
from jophiel.utils.dispatch import Signal

task_sent = Signal(providing_args=["task_id", "task","args", "kwargs","eta", "taskset"])
task_prerun = Signal(providing_args=["task_id", "task","args", "kwargs"])
task_postrun = Signal(providing_args=["task_id", "task","args", "kwargs", "retval"])
task_failure = Signal(providing_args=["task_id", "exception","args", "kwargs", "traceback","einfo"])


before_process= Signal(providing_args=["task_id", "task","args", "kwargs","eta", "taskset"])
before_process= Signal(providing_args=["task_id", "task","args", "kwargs","eta", "taskset"])