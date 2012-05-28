import os 
def setup_loader():
    os.environ.setdefault("CELERY_LOADER", "jophiel.schedule.loaders.DjangoLoader")
    
    # Importing this module enables the Celery Django loader.
setup_loader()

from celery import current_app as celery  # noqa
