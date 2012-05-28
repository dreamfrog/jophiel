'''
Created on 2012-5-2

@author: lzz
'''

from urlparse import urlparse

def parse_url(url):
    port = path = auth = userid = password = None
    
    #scheme, netloc, path, params, query, fragment
    parts= urlparse(url)
    netloc = parts.netloc
    if '@' in netloc:
        auth, _, netloc = parts.netloc.partition('@')
        userid, _, password = auth.partition(':')
    hostname, _, port = netloc.partition(':')
    path = parts.path or ""
    if path and path[0] == '/':
        path = path[1:]
    port = port and int(port) or port
    
    return (hostname,port,userid,password,path)