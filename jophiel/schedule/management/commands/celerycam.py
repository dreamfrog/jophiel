"""

Shortcut to the Django snapshot service.

"""
from __future__ import absolute_import

from celery.bin import celeryev

from jophiel.schedule.app import app
from jophiel.schedule.management.base import CeleryCommand

ev = celeryev.EvCommand(app=app)


class Command(CeleryCommand):
    """Run the celery curses event viewer."""
    options = (CeleryCommand.options
             + ev.get_options()
             + ev.preload_options)
    help = 'Takes snapshots of the clusters state to the database.'

    def handle(self, *args, **options):
        """Handle the management command."""
        options["camera"] = "jophiel.snapshot.Camera"
        ev.run(*args, **options)
