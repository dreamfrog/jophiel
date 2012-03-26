"""
The Extension Manager

See documentation in docs/topics/extensions.rst
"""
from scrapy.middleware import MiddlewareManager

class ExtensionManager(MiddlewareManager):
    component_name = 'extention manager'

