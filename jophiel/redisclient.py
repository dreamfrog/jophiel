'''
Created on 2012-2-23

@author: lzz
'''

import redis
import settings 

pool = redis.ConnectionPool(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)

def get_redis():
    password = settings.REDIS_PASSWORD
    r = redis.Redis(connection_pool=pool) 
    if password:
        r.auth(password)
    return r

client = get_redis()