'''
Created on 2012-3-19

@author: lzz
'''
import re
import threading

from itty import get,post,put,delete, run_itty
from itty import REQUEST_MAPPINGS
from itty import WSGI_ADAPTERS
from itty import add_slash

"""Registers a method as capable of processing method requests."""
def put_request(method_type,url,method):
    
    if type not in REQUEST_MAPPINGS:
        raise RuntimeError("error,method type[%s] is wrong"%method_type)
    
    re_url = re.compile("^%s$" % add_slash(url))
    REQUEST_MAPPINGS[method_type].append((re_url, url, method))
    

class ServerThread(threading.Thread):
    def __init__(self, host='localhost', port=9990,default_type = "wsgiref"):
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
        self.type = default_type
       
    def run(self):
        threadname = threading.currentThread().getName()
        if not self.type in WSGI_ADAPTERS:
            raise RuntimeError("Server '%s' is not a valid server. Please choose a different server." % self.type)
        
        WSGI_ADAPTERS[self.type](self.host, self.port)
        
        