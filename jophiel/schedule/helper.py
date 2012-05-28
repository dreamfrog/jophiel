# -- XXX This module must not use translation as that causes
# -- a recursive loader import!
from __future__ import absolute_import

from datetime import datetime

from django.conf import settings

# Database-related exceptions.
from django.db import DatabaseError
try:
    import MySQLdb as mysql
    _my_database_errors = (mysql.DatabaseError, )
except ImportError:
    _my_database_errors = ()      # noqa
try:
    import psycopg2 as pg
    _pg_database_errors = (pg.DatabaseError, )
except ImportError:
    _pg_database_errors = ()      # noqa
try:
    import sqlite3
    _lite_database_errors = (sqlite3.DatabaseError, )
except ImportError:
    _lite_database_errors = ()    # noqa
try:
    import cx_Oracle as oracle
    _oracle_database_errors = (oracle.DatabaseError, )
except ImportError:
    _oracle_database_errors = ()  # noqa

DATABASE_ERRORS = ((DatabaseError, ) +
                   _my_database_errors +
                   _pg_database_errors +
                   _lite_database_errors +
                   _oracle_database_errors)

try:
    from django.utils import timezone

    def make_aware(value):
        if getattr(settings, "USE_TZ", False):
            default_tz = timezone.get_default_timezone()
            value = timezone.make_aware(value, default_tz)
        return value

    def make_naive(value):
        if getattr(settings, "USE_TZ", False):
            default_tz = timezone.get_default_timezone()
            value = timezone.make_naive(value, default_tz)
        return value

    def now():
        return timezone.localtime(timezone.now())

except ImportError:
    now = datetime.now
    make_aware = make_naive = lambda x: x

from functools import wraps
from itertools import count
from django.db import transaction

def transaction_retry(max_retries=1):
    """Decorator for methods doing database operations.

    If the database operation fails, it will retry the operation
    at most ``max_retries`` times.

    """
    def _outer(fun):

        @wraps(fun)
        def _inner(*args, **kwargs):
            _max_retries = kwargs.pop("exception_retry_count", max_retries)
            for retries in count(0):
                try:
                    return fun(*args, **kwargs)
                except Exception:   # pragma: no cover
                    # Depending on the database backend used we can experience
                    # various exceptions. E.g. psycopg2 raises an exception
                    # if some operation breaks the transaction, so saving
                    # the task result won't be possible until we rollback
                    # the transaction.
                    if retries >= _max_retries:
                        raise
                    transaction.rollback_unless_managed()

        return _inner

    return _outer


def update_model_with_dict(obj, fields):
    [setattr(obj, attr_name, attr_value)
        for attr_name, attr_value in fields.items()]
    obj.save()
    return obj

from django.db import models
from django.db.models.query import QuerySet
from django.db import transaction, connection
try:
    from django.db import connections, router
except ImportError:  # pre-Django 1.2
    connections = router = None  # noqa
    
class ExtendedQuerySet(QuerySet):

    def update_or_create(self, **kwargs):
        obj, created = self.get_or_create(**kwargs)

        if not created:
            fields = dict(kwargs.pop("defaults", {}))
            fields.update(kwargs)
            update_model_with_dict(obj, fields)

        return obj


class ExtendedManager(models.Manager):

    def get_query_set(self):
        return ExtendedQuerySet(self.model)

    def update_or_create(self, **kwargs):
        return self.get_query_set().update_or_create(**kwargs)

    def connection_for_write(self):
        if connections:
            return connections[router.db_for_write(self.model)]
        return connection

    def connection_for_read(self):
        if connections:
            return connections[self.db]
        return connection

    def current_engine(self):
        try:
            return settings.DATABASES[self.db]["ENGINE"]
        except AttributeError:
            return settings.DATABASE_ENGINE

class TxIsolationWarning(UserWarning):
    pass