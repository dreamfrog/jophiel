'''
Created on 2012-5-2

@author: lzz
'''

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Spider(models.Model):
    
    name = models.CharField( max_length=200, unique=True,primary_key =True)
    description = models.TextField(default="")
    params = models.TextField(default="{}")
    urls = models.TextField(default="")
    
    create_time = models.DateTimeField(auto_now=True)


