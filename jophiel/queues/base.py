'''
Created on 2012-3-23

@author: lzz
'''

import json
       
class TaskMessage(object):
    
    @classmethod
    def encode(cls, item):
        return json.dumps(item)

    @classmethod
    def decode(cls, item):
        if isinstance(item, basestring):
            ret = json.loads(item)
            return ret
        return None

class BaseQueue(object):
    def __init__(self,backend,queue):
        self.conn = 
        self.client = 
