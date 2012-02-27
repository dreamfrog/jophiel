from .py_redis import RedisBackend

def get_backend(host='localhost', port=6379, db=0):
    return RedisBackend(host, port, db)
