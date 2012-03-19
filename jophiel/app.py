'''
Created on 2012-2-28

@author: lzz
'''
import redis
import settings 
import inspect

from jophiel.errors import NoRegisterError
from jophiel.utils import get_cls_by_name
from jophiel.utils import Registry

import logging

#db = DatastoreProxy()

pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def get_redis():
    password = settings.REDIS_PASSWORD
    r = redis.Redis(connection_pool=pool) 
    if password:
        r.auth(password)
    return r

client = get_redis()

def getlogger():
    logger = logging.getLogger()
    hdlr = logging.FileHandler(settings.LOG_FILE)
    formatter = logging.Formatter('[%(asctime)s]%(levelname)-8s"%(message)s"', '%Y-%m-%d %a %H:%M:%S') 
    
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.NOTSET)
    return logger

logger = getlogger()

        
def import_tasks(tasks): 
    tasklists = settings.TASK_LIST
    for task_cls in tasklists:
        cls = get_cls_by_name(task_cls)
        print "--import__",cls
        #register tasks
        task_name = cls.name
        if task_name not in tasks:
            tasks.register(cls)
                   
# Global task registry
tasks = Registry()
import_tasks(tasks)


