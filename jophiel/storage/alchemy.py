'''
Created on 2012-5-29

@author: lzz
'''
from django.conf import settings
from django.db import connection
from sqlalchemy import create_engine, MetaData, exceptions
from sqlalchemy.sql import operators
from sqlalchemy import *
from sqlalchemy.sql import select
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


class Wrapper(object):
    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, attr):
        if attr in ['commit', 'rollback']:
            return nullop
        obj = getattr(self.obj, attr)
        if attr not in ['cursor', 'execute']:
            return obj
        if attr == 'cursor':
            return type(self)(obj)
        return self.wrapper(obj)

    def wrapper(self, obj):
        "Implement if you need to make your customized wrapper"
        return obj

    def __call__(self, *a, **kw):
        self.obj = self.obj(*a, **kw)
        return self


def nullop(*a, **kw):
    return


class SqliteWrapper(Wrapper):

    def wrapper(self, obj):
        return sqlite_wrapper(obj)


def sqlite_wrapper(func):
    from django.db.backends.sqlite3.base import Database

    def null_converter(s):
        return s

    def wrapper(*a, **kw):
        converter = Database.converters.pop('DATETIME')
        Database.register_converter("datetime", null_converter)
        res = func(*a, **kw)
        Database.register_converter("DATETIME", converter)
        return res

    return wrapper
