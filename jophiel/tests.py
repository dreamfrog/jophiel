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

class JobTests(TestCase):
    def setUp(self):
        self.job = JobBase("test","test")
    def testApply(self):
        schedule.apply(self.job)

if __name__=="__main__":
    unittest.main()