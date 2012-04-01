'''
Created on 2012-2-28

@author: lzz
'''

import unittest
from unittest import TestCase
from jophiel.db.models import BaseModel
from jophiel.db.field import *
from jophiel.jobs.base import JobBase
import random 
from jophiel import schedule 

from jophiel.backend import tests
from jophiel.backend.connection import BrokerConnection


if __name__=="__main__":
    with BrokerConnection("redis://localhost:6379//") as conn:
    
        #: SimpleQueue mimics the interface of the Python Queue module.
        #: First argument can either be a queue name or a kombu.Queue object.
        #: If a name, then the queue will be declared with the name as the queue
        #: name, exchange name and routing key.
        with conn.SimpleQueue("kombu_demo") as queue:
            while True:
                message = queue.get(block=True, timeout=10)
                if message:
                    print message.ack()
                    print(message.payload)
                else:
                    print "empty"

    
    