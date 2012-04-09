# -*- coding: utf-8 -*-

from django import forms
from django.conf import settings
from django.contrib import admin
from django.core.exceptions import ImproperlyConfigured
from django.db.models.options import get_verbose_name
from django.forms.models import ModelForm
from django.utils.encoding import smart_str
from django.utils.translation import ugettext_lazy as _

class BlockBaseMetaclass(forms.MediaDefiningClass):
    """
    Ensure the CMSPlugin subclasses have sane values and set some defaults if 
    they're not given.
    """
    def __new__(cls, name, bases, attrs):
        super_new = super(BlockBaseMetaclass, cls).__new__
        parents = [base for base in bases if isinstance(base, BlockBaseMetaclass)]
        if not parents:
            # If this is CMSPluginBase itself, and not a subclass, don't do anything
            return super_new(cls, name, bases, attrs)
        new_plugin = super_new(cls, name, bases, attrs)
        
        # validate the template:
        #if not hasattr(new_plugin, 'render_template'):
        #    raise ImproperlyConfigured(
        #        "CMSPluginBase subclasses must have a render_template attribute"
        #    )
        # Set default name
        if not new_plugin.name:
            new_plugin.name = get_verbose_name(new_plugin.__name__)
        return new_plugin


