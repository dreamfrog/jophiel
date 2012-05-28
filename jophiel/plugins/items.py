
from django.utils.translation import ugettext, ugettext_lazy as _

from . import params
from .params import ConfigDict

class RegisteredItem(object):
    name = None
    placed_at = None
    is_fixed = False
    fixed_place = False
    # caching parameters
    is_cached = False
    cache_timeout = 0
    cache_only_anonymous = False
    cache_vary_on_user = False
    cache_vary_on_url = False
    cache_vary_on_language = True
    # fields for blocks related to contents
    content = ""
    overwrite_if_place = True
    overwrite_always = False

    def get_config(self):
        return {}

    def __unicode__(self):
        return self.name
    
    def update(self,**kwargs):
        self.cache_timeout = kwargs.get('timeout', 0)
        self.cache_only_anonymous = kwargs.get('only_anonymous', False)
        self.cache_vary_on_language = kwargs.get('vary_on_language', True)
        self.cache_vary_on_url = kwargs.get('vary_on_url', False)
        self.cache_vary_on_user = kwargs.get('vary_on_user', False)
        self.is_cached = kwargs.get('enabled', False)

class RegistrableItem(object):
    """ Base class for all registered objects """

    name = None  # to be overriden in subclasses
    verbose_name = None  # to be overriden in subclasses
    help_text = None  # to be overriden in subclasses
    config_params = []  # configuration parameters, to be overriden
    singleton = False  # only allow one registered item per class
    active_by_default = True  # will be active when registered

    @classmethod
    def get_class_name(cls):
        return cls.__name__

    @classmethod
    def get_module(cls):
        return cls.__module__

    @classmethod
    def get_extended_attrs(cls):
        return {}

    def __init__(self, reg_item):
        self.reg_item = reg_item

    def _config_dict(self, config):
        return ConfigDict(self.config_params, config)

    def get_config(self):
        registered_item = self.get_registered_item()
        return self._config_dict(registered_item.get_config())

    def has_config(self):
        return bool(self.config_params)

    def get_registered_item(self):
        return self.reg_item


