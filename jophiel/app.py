'''
Created on 2012-2-28

@author: lzz
'''
import redis
import settings 

from jophiel.db.test_backend import DatastoreProxy
from jophiel.utils import Registry
from jophiel.logger import get_logger
from jophiel.utils import get_cls_by_name

db = DatastoreProxy()
pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


def get_redis(settings,pool):
    password = settings.REDIS_PASSWORD
    print redis.__file__
    r = redis.Redis(connection_pool=pool) 
    if password:
        r.auth(password)
    return r

client = get_redis(settings,pool)
logger = get_logger("jophiel")

def import_tasks(tasks,tasklists): 
    for task_cls in tasklists:
        cls = get_cls_by_name(task_cls)
        print "--import__",cls
        #register tasks
        task_name = cls.name
        if task_name not in tasks:
            tasks.register(cls)     
# Global task registry
tasks = Registry()
import_tasks(tasks,settings.TASK_LIST)
