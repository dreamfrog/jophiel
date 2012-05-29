from optparse import make_option
from django.core.management.base import NoArgsCommand
from news.models import Article

class Command(NoArgsCommand):
    help = "Can be run as a cronjob or directly to purge old articles."

    def handle_noargs(self, **options):
        """
        Update the database with articles
        """
        Article.objects.filter(expired=True).delete()
