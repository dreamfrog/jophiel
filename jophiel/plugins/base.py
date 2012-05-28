import hashlib
from time import time

from django.conf import settings
from django.core import signals
from django.core.cache import cache
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.http import urlquote
from django.utils.log import getLogger
from django.utils.translation import get_language, ugettext as _
from django import forms

from django.core.exceptions import ImproperlyConfigured
from django.db.models.options import get_verbose_name

from . import params
from .items import RegistrableItem

logger = getLogger('jophiel.plugins')


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
        
        # Set default name
        if not new_plugin.name:
            new_plugin.name = get_verbose_name(new_plugin.__name__)
        return new_plugin

class BaseBlock(RegistrableItem):
    
    __metaclass__ = BlockBaseMetaclass
    is_addable = True
    config_params = [
        params.Single(name='css_class', label=_('css class to add to this block'), default=''),
        ]

    def __init__(self, reg_item):
        super(BaseBlock, self).__init__(reg_item)

    def get_rendered_content(self, request, render_args):
        """ render the block content, using cached content is needed """
        if settings.DEBUG:
            start = time()
        rendered_content = self.render(*render_args)
        if settings.DEBUG:
            stop = time()
            duration = stop - start
            block_id = '%s.%s:%s' % (self.get_module(), self.get_class_name(), self.reg_item.name)
            logger.debug('(%.3f) %s;' % (duration, block_id),extra={'duration': duration, 'block': block_id}
            )
        return rendered_content

    def render_block(self, request, template_name='block.html', block_title=None,
                     context=None):
        if context is None:
            context = {}
        registered_block = self.get_registered_item()
        css_class = self.get_config().get('css_class', None)
        css_class = css_class and css_class.get_value() or ''
        block_context = {
            'block_name': registered_block.name,
            'placed_at': registered_block.placed_at,
            'fixed_place': getattr(registered_block, 'fixed_place', False),
            'block_title': block_title or registered_block.name,
            'block': registered_block,
            'css_class': css_class,
            'has_config': self.has_config(),
        }
        block_context.update(context)
        rendered_content = render_to_string(template_name, block_context,
                                            context_instance=RequestContext(request))
        return rendered_content

