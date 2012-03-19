'''
Created on 2012-3-16

@author: lzz
'''

import uuid
from jophiel.utils import fun_takes_kwargs
from jophiel.tasks.engine import TaskEngine
from jophiel.tasks import TaskResult
from jophiel.utils import ExceptionInfo
from jophiel import app

def apply(job):
    """Execute this task locally, by blocking until the task returns.
    """
    if not job.task_id:
        job.task_id = uuid.uuid4().hex
    task_id = job.task_id
    task_name = job.task_name
    queue = job.queue
    # Make sure we get the task instance, not class.
    taskcls = app.tasks[task_name]
    default_kwargs = {
                      "task_name": taskcls.name,
                      "task_id": job.task_id,
                      }
    options = job.options
    supported_keys = fun_takes_kwargs(taskcls.run, default_kwargs)
    extend_with = dict((key, val) for key, val in default_kwargs.items()
                                if key in supported_keys)
    args = job.args
    kwargs = options.copy()
    kwargs.update(extend_with)

    engine = TaskEngine(task_name, task_id, queue, args, kwargs, task=taskcls)
    retval = engine.execute()
    
    if isinstance(retval, ExceptionInfo):
        retval = retval.exception
    return TaskResult(job,task_id, retval, engine.status,
                       traceback=engine.strtb)    
