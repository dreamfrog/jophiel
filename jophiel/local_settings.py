'''
Created on 2012-4-6

@author: lzz
'''
import os

LOG_FILE = "jophiel.log"

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_PASSWORD = ""

HBASE_PROFILE = True
HBASE_THRIFT_HOST = "localhost"
HBASE_THRIFT_PORT = 9090
HBASE_DEFALT_MAX_VERSIONS = 3


DEFAULT_CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'utf-8'

# Encoding of files read from disk (template and initial SQL files).
FILE_CHARSET = 'utf-8'


TASK_LIST = [
             "jophiel.contrib.tasks.test.TestTask",
             ]

QUEUE_BACKEND = "redis://localhost:6379//"

BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis"
CELERY_REDIS_HOST = "localhost"
CELERY_REDIS_PORT = 6379
CELERY_REDIS_DB = 0

CELERY_IMPORTS = ('feeds.tasks','news.tasks')

import djcelery
djcelery.setup_loader()

LOGIN_URL = "/login"

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"

# Set your DSN value
SENTRY_DSN = 'http://5414a038f9bd491db1a7372f1ce272d6:6a76fafcfebb41e98c80e6fb0e2e4ec4@127.0.0.1:9000/2'

DEBUG_TOOLBAR_CONFIG = {"INTERCEPT_REDIRECTS": False}

FROIDE_CONFIG = { 
    "create_new_publicbody": True,
    "publicbody_empty": True,
    "user_can_hide_web": True,
    "public_body_officials_public": True,
    "public_body_officials_email_public": False,
    "request_public_after_due_days": 14, 
    "payment_possible": True,
    "currency": "Euro",
    "default_law": 1
}

SITE_URL = 'http://localhost:8000'

USING_PASSWORD_REGISTER = True

TASTYPIE_FULL_DEBUG = True
