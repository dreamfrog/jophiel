'''
Created on 2012-2-28

@author: lzz
'''

from jophiel.db.models import BaseModel
from jophiel.db.field import StringField
from jophiel.db.field import StringField

class HttpRequest(BaseModel):
    url = StringField()
    last_modify_time = StringField()
    