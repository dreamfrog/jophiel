'''
Created on 2012-3-15

@author: lzz
'''
import unittest
from unittest import TestCase
import random 

from jophiel.backend.connection import BrokerConnection

class TestQueue(TestCase):
    
    def setUp(self):pass
        
    def setDown(self):pass
    
    def testQueue(self):
        with BrokerConnection("redis://localhost:6379//") as conn:
            with conn.SimpleQueue("kombu_demo") as queue:
                queue.put({"hello": "world"}, serializer="json")

    