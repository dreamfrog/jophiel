"""
sentry.processors.base
~~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2010-2012 by the Sentry Team, see AUTHORS for more details.
:license: BSD, see LICENSE for more details.
"""
import logging

from django.db import transaction

from sentry.plugins import plugins

__all__ = ('send_group_processors',)


def send_group_processors(group, **kwargs):
    for inst in plugins.all():
        try:
            inst.post_process(group=group, **kwargs)
        except Exception, e:
            transaction.rollback_unless_managed(using=group._state.db)
            logger = logging.getLogger('sentry.plugins')
            logger.exception('Error processing post_process() on %r: %s', inst.__class__, e)
