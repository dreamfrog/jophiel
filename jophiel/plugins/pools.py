# -*- coding: utf-8 -*-

from django.core.exceptions import ImproperlyConfigured

from jophiel.utils.cms.django_load import load

from jophiel.exceptions import PluginAlreadyRegistered, PluginNotRegistered
from .base import BaseBlock

PLUGIN_MODULE_NAME = "plugins"

class BlockPool(object):
    def __init__(self):
        self.plugins = {}
        self.discovered = False

    def discover_plugins(self):
        if self.discovered:
            return
        self.discovered = True
        load(PLUGIN_MODULE_NAME)

    def register_plugin(self, plugin):
        """
        Registers the given plugin(s).
        If a plugin is already registered, this will raise PluginAlreadyRegistered.
        """
        if not isinstance(plugin, BaseBlock):
            raise ImproperlyConfigured(
                    "CMS Plugins must be subclasses of CMSPluginBase, %r is not."% plugin
            )
        plugin_name = plugin.name
        if plugin_name in self.plugins:
            raise PluginAlreadyRegistered(
                "Cannot register %r, a plugin with this name (%r) is already "
                "registered." % (plugin, plugin_name)
            )
        plugin.value = plugin_name
        self.plugins[plugin_name] = plugin

    def unregister_plugin(self, plugin):
        """
        Unregisters the given plugin(s).

        If a plugin isn't already registered, this will raise PluginNotRegistered.
        """
        plugin_name = plugin.name
        if plugin_name not in self.plugins:
            raise PluginNotRegistered(
                'The plugin %r is not registered' % plugin
            )
        del self.plugins[plugin_name]
        
    def get_plugin(self, name):
        """
        Retrieve a plugin from the cache.
        """
        self.discover_plugins()
        return self.plugins[name]


