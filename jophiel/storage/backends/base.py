'''
Created on 2012-2-28

@author: lzz
'''
import uuid

class NoImplemented(Exception):
    pass

class DoesNotExist(Exception):
    pass

class DuplicateKeyError(Exception):
    pass

class IllegalParameters(Exception):
    pass


class TimedOutException(Exception):
    pass

class AllServersUnavailable(Exception):
    """Raised when none of the servers given to a pool can be connected to."""

class NoConnectionAvailable(Exception):
    """Raised when there are no connections left in a pool."""

class MaximumRetryException(Exception):
    """
    Raised when a :class:`ConnectionWrapper` has retried the maximum
    allowed times before being returned to the pool; note that all of
    the retries do not have to be on the same operation.
    """

class InvalidRequestError(Exception):
    """
    Pycassa was asked to do something it can't do.

    This error generally corresponds to runtime state errors.
    """

class BaseBackend(object):
    
    def generate_key(self, schema):
        return uuid.uuid4().hex