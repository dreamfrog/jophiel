'''
Created on 2012-2-28

@author: lzz
'''

import unittest
from unittest import TestCase
from jophiel.schemas import HttpRequest

class TestModel(TestCase):
    
    def setUp(self):pass
        
    def setDown(self):pass
    
    def testEnqueue(self):
        table_name = "dianping"
        url = "http://www.dianping.com/shop/223223.html"
        request = HttpRequest(table_name,url)
        request.create_schema()
        
        request.url = url
        request.last_modify_time = "2011.12.12 12:12:12-----"
        request.save()
        