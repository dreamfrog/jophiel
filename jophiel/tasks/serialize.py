'''
Created on 2012-5-17

@author: lzz
'''

import pickle

def _pickle_serialize(obj):
    try:
        return pickle.dumps(obj, protocol=2)
    except pickle.PicklingError, e:
        raise ValueError(str(e))
    
def _pickle_deserialize(s):
    return pickle.loads(s)


dumps = _pickle_serialize
loads = _pickle_deserialize