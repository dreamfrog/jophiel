'''
Created on 2012-4-13

@author: lzz
'''

def utf8(value):
    """Return the value as a UTF-8 string."""
    if type(value) == type(u''):
        return value.encode("utf-8")
    else:
        try:
            return unicode(value, "utf-8").encode("utf-8")
        except UnicodeError:
            try:
                return unicode(value, "iso-8859-1").encode("utf-8")
            except UnicodeError:
                return unicode(value, "ascii", "replace").encode("utf-8")