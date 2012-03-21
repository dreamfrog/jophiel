import datetime, time
from base64 import b64encode

from base import BaseBackend
from jophiel.app import client
import json


class RedisBackend(BaseBackend):
    """Extends the ``BaseBackend`` to provide a Redis backend for failed jobs."""

    def save(self, resq=None):
        """Saves the failed Job into a "failed" Redis queue preserving all its original enqueud info."""
        data = {
            'failed_at' : datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S'),
            'payload'   : self._payload,
            'exception' : self._exception.__class__.__name__,
            'error'     : self._parse_message(self._exception),
            'backtrace' : self._parse_traceback(self._traceback),
            'queue'     : self._queue
        }
        if self._worker:
            data['worker'] = self._worker
        data = json.dumps(data)
        client.rpush('resque:failed', data)

    @classmethod
    def count(cls, resq):
        return int(resq.redis.llen('resque:failed'))

    @classmethod
    def all(cls, start=0, count=1):
        items = client.lrange('resque:failed', start, count) or []

        ret_list = []
        for i in items:
            failure = json.loads(i)
            failure['redis_value'] = b64encode(i)
            ret_list.append(failure)
        return ret_list

    @classmethod
    def clear(cls):
        return client.delete('resque:failed')

