'''
Created on 2012-5-25

@author: lzz
'''
import time
import socket
import sys

from thrift.transport import TTransport
from thrift.transport import TSocket
from thrift.protocol import TBinaryProtocol

from thrift import Thrift
from .hbase import Hbase
from .base import *
from .connection import Connection

_BASE_BACKOFF = 0.01

class ConnectionWrapper(Connection):
    """
    Creates a wrapper for a :class:`~.pycassa.connection.Connection`
    object, adding pooling related functionality while still allowing
    access to the thrift API calls.

    These should not be created directly, only obtained through
    Pool's :meth:`~.ConnectionPool.get()` method.
    """

    # These mark the state of the connection so that we can
    # check to see that they are not returned, checked out,
    # or disposed twice (or from the wrong state).
    _IN_QUEUE = 0
    _CHECKED_OUT = 1
    _DISPOSED = 2

    def __init__(self, pool, max_retries, *args, **kwargs):
        self._pool = pool
        self._retry_count = 0
        self.max_retries = max_retries
        self.info = {}
        self.starttime = time.time()
        self.operation_count = 0
        self._state = ConnectionWrapper._CHECKED_OUT
        Connection.__init__(self, *args, **kwargs)
        self._pool._notify_on_connect(self)

    def return_to_pool(self):
        """
        Returns this to the pool.

        This has the same effect as calling :meth:`ConnectionPool.put()`
        on the wrapper.

        """
        self._pool.put(self)

    def _checkin(self):
        if self._state == ConnectionWrapper._IN_QUEUE:
            raise InvalidRequestError("A connection has been returned to "
                    "the connection pool twice.")
        elif self._state == ConnectionWrapper._DISPOSED:
            raise InvalidRequestError("A disposed connection has been returned "
                    "to the connection pool.")
        self._state = ConnectionWrapper._IN_QUEUE

    def _checkout(self):
        if self._state != ConnectionWrapper._IN_QUEUE:
            raise InvalidRequestError("A connection has been checked "
                    "out twice.")
        self._state = ConnectionWrapper._CHECKED_OUT

    def _is_in_queue_or_disposed(self):
        ret = self._state == ConnectionWrapper._IN_QUEUE or \
              self._state == ConnectionWrapper._DISPOSED
        return ret

    def _dispose_wrapper(self, reason=None):
        if self._state == ConnectionWrapper._DISPOSED:
            raise InvalidRequestError("A connection has been disposed twice.")
        self._state = ConnectionWrapper._DISPOSED

        self.close()
        self._pool._notify_on_dispose(self, msg=reason)

    def _replace(self, new_conn_wrapper):
        """
        Get another wrapper from the pool and replace our own contents
        with its contents.

        """
        self.server = new_conn_wrapper.server
        self.transport = new_conn_wrapper.transport
        self._iprot = new_conn_wrapper._iprot
        self._oprot = new_conn_wrapper._oprot
        self.info = new_conn_wrapper.info
        self.starttime = new_conn_wrapper.starttime
        self.operation_count = new_conn_wrapper.operation_count
        self._state = ConnectionWrapper._CHECKED_OUT

    @classmethod
    def _retry(cls, f):
        def new_f(self, *args, **kwargs):
            self.operation_count += 1
            self.info['request'] = {'method': f.__name__, 'args': args, 'kwargs': kwargs}
            try:
                allow_retries = kwargs.pop('allow_retries', True)
                if kwargs.pop('reset', False):
                    self._pool._replace_wrapper() # puts a new wrapper in the queue
                    self._replace(self._pool.get()) # swaps out transport
                result = f(self, *args, **kwargs)
                self._retry_count = 0 # reset the count after a success
                return result
            except Thrift.TApplicationException, app_exc:
                self.close()
                self._pool._decrement_overflow()
                self._pool._clear_current()
                raise app_exc
            except (Thrift.TException,
                    socket.error, IOError, EOFError), exc:
                self._pool._notify_on_failure(exc, server=self.server, connection=self)

                self.close()
                self._pool._decrement_overflow()
                self._pool._clear_current()

                self._retry_count += 1
                if (not allow_retries or
                    (self.max_retries != -1 and self._retry_count > self.max_retries)):
                    raise MaximumRetryException('Retried %d times. Last failure was %s: %s' %
                                                (self._retry_count, exc.__class__.__name__, exc))
                # Exponential backoff
                time.sleep(_BASE_BACKOFF * (2 ** self._retry_count))

                kwargs['reset'] = True
                return new_f(self, *args, **kwargs)

        new_f.__name__ = f.__name__
        return new_f

    def __str__(self):
        return "<ConnectionWrapper %s>" % (self.server,)

retryable = ('isTableEnabled', 'getTableNames', 'getColumnDescriptors', 'getTableRegions', 'createTable',
             'deleteTable', 'get', 'getVer', 'getVerTs',
             'getRow', 'getRowWithColumns', 'getRowTs', 'getRowWithColumnsTs', 'getRows',
             'getRowsWithColumns','getRowsTs','getRowsWithColumnsTs','mutateRow','mutateRowTs','mutateRows',
             'mutateRowsTs','atomicIncrement','deleteAll','deleteAllTs','deleteAllRow','deleteAllRowTs','scannerOpenWithScan',
             'scannerOpen','scannerOpenWithStop','scannerOpenWithPrefix','scannerOpenTs','scannerOpenWithStopTs',
             'scannerGet','scannerGetList','scannerClose',
             )
for fname in retryable:
    new_f = ConnectionWrapper._retry(getattr(Connection, fname))
    setattr(ConnectionWrapper, fname, new_f)