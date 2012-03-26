'''
Created on 2012-3-23

@author: lzz
'''

class BaseMeta(type):
    def __new__(cls, name, bases, attrs):
        super_new = super(BaseMeta, cls).__new__
        module = attrs.pop('__module__')
        new_class = super_new(cls, name, bases, {'__module__': module})
        
        #setattr(new_class, 'redis', client)

        # Add all attributes to the class.
        for obj_name, obj in attrs.iteritems():
            setattr(new_class, obj_name, obj)
        return new_class
 
class BaseStat(object):
    __metaclass__ = BaseMeta