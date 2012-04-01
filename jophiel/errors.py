'''
Created on 2012-2-28

@author: lzz
'''

class NoQueueError(Exception):
    pass

class NoRegisterError(Exception):
    pass

class NotImplementError(Exception):
    pass


class NoRedisConnectionException(Exception):
    pass

class NoSuchJobError(Exception):
    pass

class UnpickleError(Exception):
    pass