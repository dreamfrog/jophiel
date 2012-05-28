'''
Created on 2012-5-2

@author: lzz
'''

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Spider(models.Model):
    
    name = models.CharField( max_length=30, unique=True)
    description = models.TextField(default="")
    params = models.TextField(default="{}")
    urls = models.TextField(default="")
    
    domains = models.TextField(default="[]")
    rules = models.TextField(default = "{}")
    settings = models.TextField(default="{}")
    tablename = models.CharField(max_length=20)
    storagename = models.CharField(max_length=20)
    
    create_time = models.DateTimeField(auto_now=True)
    


