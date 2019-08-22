# THIS FILE CAN BE REFERENCED VIA ENVIRONMENT VARIABLE.
#
# Namespace configuration for all of artifice.scraper
# Handles the scraper api and celery task manager
#    as well as rabbitmq, amqp, rcp, and Redis cache.
import os
import sys
# BASE_DIR:///artifice/scraper/
loc = os.path.dirname(os.path.abspath(__file__))
#
# Foreground
# 
TESTING = False
URL_PREFIX = '/'

FLASK_PORT = 8080
FLASK_HOST = '0.0.0.0'
FLASK_DEBUG = False
FLASK_USE_RELOADER = False
FLASK_THREADED = True

DROP_TABLES = True

LOG_FILE = 'celery.log'
LOG_LEVEL = 'INFO'
STDOUT = True

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(loc, 'site.db'))

REDIS_URL = 'redis://password:@localhost:6379/0'
REDIS_HIT_COUNTER = 'HIT_COUNTER'

ARGS_DEFAULT_LIMIT = 10
ARGS_DEFAULT_STATUS = ['READY', 'TASKED', 'DONE']

SUPERVISOR_ENABLED = False
SUPERVISOR_DEBUG = True
SUPERVISOR_POLITE = 3

#
# Background
#
CELERY_WORKERS = 8
CELERY_MODULE = 'background'
CELERY_BROKER = 'amqp://michael:michael123@localhost/michael_vhost'
CELERY_BACKEND = 'rpc://'
CELERY_INCLUDE = ['artifice.scraper.background.tasks']

CELERY_LOG_LEVEL = 'ERROR'
CELERY_LOG_FILE = 'celery.log'

ENDPOINT_FOR_STATUS = 'http://127.0.0.1:8080/status'
ENDPOINT_FOR_QUEUE = 'http://127.0.0.1:8080/queue'
ENDPOINT_FOR_CONTENT = 'http://127.0.0.1:8080/content'
