'''
Created on 2012-5-2

@author: lzz
'''

from django.db import models

class Spider(models.Model):
    name = models.CharField(_(u"name"), max_length=200, unique=True,
                        help_text=_(u"Spider Name,Unique"))
    params = models.TextField(_(u"Keyword arguments"),
                              blank=True, default="{}",
                              help_text=_("JSON encoded  params"))
    
    