'''
Created on 2012-4-13

@author: lzz
'''

try: 
    from xml.sax.saxutils import escape
except:
    def escape(data):
        return data.replace("&","&amp;").replace(">","&gt;").replace("<","&lt;")