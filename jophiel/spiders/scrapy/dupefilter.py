import os
from scrapy.utils.request import request_fingerprint
from scrapy.utils.job import job_dir

from scrapy.meta import SettingObject
from scrapy.meta import StringField

class BaseDupeFilter(SettingObject):

    def request_seen(self, request):
        return False

    def open(self):  # can return deferred
        pass

    def close(self, reason): # can return a deferred
        pass


class RFPDupeFilter(BaseDupeFilter):
    """Request Fingerprint duplicates filter"""
    
    job_dir = StringField(default="")
    
    def __init__(self, settings):
        super(RFPDupeFilter, self).__init__(settings)
        path = self.__job_dir(self.job_dir.to_value())
        
        self.file = None
        self.fingerprints = set()
        if path:
            self.file = open(os.path.join(path, 'requests.seen'), 'a+')
            self.fingerprints.update(x.rstrip() for x in self.file)
            
    def __job_dir(self, path):
        if path and not os.path.exists(path):
            os.makedirs(path)
        return path
    
    def request_seen(self, request):
        fp = request_fingerprint(request)
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)

    def close(self, reason):
        if self.file:
            self.file.close()
