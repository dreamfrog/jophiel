'''
Created on 2012-3-15

@author: lzz
'''

import unittest
from unittest import TestCase
from jophiel.db.models import BaseModel
from jophiel.db.field import *
import random 

class HttpRequestSchema(BaseModel):
    
    row_key = KeyField()
    url = StringField()
    last_modify_time = DateTimeField()
    body = StringField()
    

class TestModel(TestCase):pass