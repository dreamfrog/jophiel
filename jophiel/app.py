'''
Created on 2012-2-28

@author: lzz
'''
import redis
import settings 

from jophiel.db.test_backend import DatastoreProxy
from jophiel.utils import Registry
from jophiel.utils.task import import_tasks
from jophiel.utils.redis import get_redis
from jophiel.utils.logger import getlogger

db = DatastoreProxy()
pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

client = get_redis(settings,pool)
logger = getlogger(settings)
                   
# Global task registry
tasks = Registry()
import_tasks(tasks,settings.TASK_LIST)
