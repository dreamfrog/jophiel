'''
Created on 2012-5-28

@author: lzz
'''


from .models import IntervalSchedule
from .models import PeriodicTask

def create_internal_task(name,task,internal,args):
    schedule=IntervalSchedule.objects.create(every=internal,period='seconds')
    task = PeriodicTask(
              name=name,
              task=task,
              args = "[\""+args+"\"]",
              interval = schedule,
              enabled = True
            )
    task.save()
