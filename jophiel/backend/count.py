'''
Created on 2012-2-25

@author: lzz
'''

from jophiel.app import client
from jophiel.backend.base import BaseStat
from jophiel.app import logger
    
"""
A Stat class which shows the current status of the queue.
"""     

class Stats(BaseStat):
  
    def __init__(self, name):
        self.name = name

    def get(self):
        val = client.get(self.name)
        if val:
            return int(val)
        return 0

    def incr(self, ammount=1):
        client.incr(self.name, ammount)

    def decr(self, ammount=1):
        client.decr(self.name, ammount)

    def clear(self):
        client.delete(self.name)


