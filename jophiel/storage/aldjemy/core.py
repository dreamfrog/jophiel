from django.conf import settings
from django.db import connection

try:
    from sqlalchemy import create_engine, MetaData, exceptions
    from sqlalchemy.sql import operators
except ImportError, e:
    from django.core.exceptions import ImproperlyConfigured
    raise ImproperlyConfigured("Error loading sqlalchemy module: %s" % e)

from sqlalchemy.orm import scoped_session, sessionmaker

__all__ = ['get_engine', 'get_meta', 'get_tables','get_session']

kw = {"convert_unicode":True}
engine = create_engine(settings.DJANGO_SQLALCHEMY_DBURI, **kw)
engine.echo = getattr(settings, 'DJANGO_SQLALCHEMY_ECHO', False)

session = scoped_session(sessionmaker(bind=engine))

# default metadata
metadata = MetaData(bind=engine)

def get_engine():
    return engine

def get_meta():
    return metadata

def get_session():
    return session

def get_tables():
    return metadata.tables
