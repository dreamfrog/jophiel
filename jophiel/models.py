'''
Created on 2012-2-26

@author: lzz
'''
from django.db import models

"""
basic worker task models
"""
    
        
class Worker(models.Model):
    worker_id = models.TextField(null=False,unique = True)
    queue = models.TextField(null=False)
    status = models.TextField(null=False)
        
    host = models.TextField()
    ip_address = models.TextField()
    port = models.IntegerField()
    
    create_at = models.TextField()
    update_at = models.TextField()
    

class WorkerUnit(models.Model):
    workerunit_id = models.TextField(null=False,unique = True)
    #worker_id = models.ForeignKey(Worker)
    #job_id = models.ForeignKey(Job)
    
    args = models.TextField()
    kwargs = models.TextField()    
    outputs = models.TextField()

    create_at = models.TextField()
    update_at = models.TextField()    
     

    
    