# -*- coding: utf-8 -*-
# TODO: this is just stuff from utils.py - should be splitted / moved
from .i18n import get_default_language
from distutils.version import LooseVersion
from django.conf import settings
from django.core.files.storage import get_storage_class
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.functional import LazyObject
import django
import os
import urllib


def get_template_from_request(request, obj=None, no_current_page=False):
    """
    Gets a valid template from different sources or falls back to the default
    template.
    """
    template = None
    if len(settings.CMS_TEMPLATES) == 1:
        return settings.CMS_TEMPLATES[0][0]
    if "template" in request.REQUEST:
        template = request.REQUEST['template']
    if not template and obj is not None:
        template = obj.get_template()
    if not template and not no_current_page and hasattr(request, "current_page"):
        current_page = request.current_page
        if hasattr(current_page, "get_template"):
            template = current_page.get_template()
    if template is not None and template in dict(settings.CMS_TEMPLATES).keys():
        if template == settings.CMS_TEMPLATE_INHERITANCE_MAGIC and obj:
            # Happens on admin's request when changing the template for a page
            # to "inherit".
            return obj.get_template()
        return template    
    return settings.CMS_TEMPLATES[0][0]


def get_language_from_request(request, current_page=None):
    """
    Return the most obvious language according the request
    """
    language = request.REQUEST.get('language', None)
    if language:
        if not language in dict(settings.CMS_LANGUAGES).keys():
            language = None
    if language is None:
        language = getattr(request, 'LANGUAGE_CODE', None)
    if language:
        if not language in dict(settings.CMS_LANGUAGES).keys():
            language = None


    if language is None:
        # language must be defined in CMS_LANGUAGES, so check first if there
        # is any language with LANGUAGE_CODE, otherwise try to split it and find
        # best match
        language = get_default_language()

    return language


"""
The following class is taken from https://github.com/jezdez/django/compare/feature/staticfiles-templatetag
and should be removed and replaced by the django-core version in 1.4
"""
default_storage = 'django.contrib.staticfiles.storage.StaticFilesStorage'
if LooseVersion(django.get_version()) < LooseVersion('1.3'):
    default_storage = 'staticfiles.storage.StaticFilesStorage'


class ConfiguredStorage(LazyObject):
    def _setup(self):
        self._wrapped = get_storage_class(getattr(settings, 'STATICFILES_STORAGE', default_storage))()

configured_storage = ConfiguredStorage()

def cms_static_url(path):
    '''
    Helper that prefixes a URL with STATIC_URL and cms
    '''
    if not path:
        ''
    return configured_storage.url(os.path.join('cms', path))
