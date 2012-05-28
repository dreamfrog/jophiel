"""

Start the celery clock service from the Django management command.

"""
from __future__ import absolute_import

from celery.bin import celerybeat

from jophiel.app import app
from jophiel.management.base import CeleryCommand

beat = celerybeat.BeatCommand(app=app)


class Command(CeleryCommand):
    """Run the celery periodic task scheduler."""
    options = (CeleryCommand.options
             + beat.get_options()
             + beat.preload_options)
    help = 'Runs the Celery periodic task scheduler'

    def handle(self, *args, **options):
        beat.run(*args, **options)
