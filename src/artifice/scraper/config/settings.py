# Namespace configuration for all of artifice.scraper
# Handles the scraper api and celery task manager
#    as well as rabbitmq, amqp, rcp, and Redis cache.
import os
import sys
loc = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(loc)
# BASE_DIR:///artifice/scraper/
#################################
# Global -- Variables
#################################
_eth0 = '0.0.0.0'
_exposed_port = 8080
_redis_pword = 'password'
_redis_host = 'localhost'
_celery_broker_uname = 'michael'
_celery_broker_pword = 'michael123'
_celery_broker_host = 'localhost'
_celery_broker_virtual_host = 'michael_vhost'
#################################
# Foreground -- Flask
#################################
TESTING = False
URL_PREFIX = ''

FLASK_PORT = _exposed_port
FLASK_HOST = '0.0.0.0'
FLASK_DEBUG = False
FLASK_USE_RELOADER = False
FLASK_THREADED = True

DROP_TABLES = True

LOG_FILE = 'celery.log'
LOG_LEVEL = 'INFO'
STDOUT = True

# DASHBOARD_CONFIG =

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'site.db'))

REDIS_URL = 'redis://{}:@{}:6379/0'.format(_redis_pword, _redis_host)
REDIS_HIT_COUNTER = 'HIT_COUNTER'

ARGS_DEFAULT_LIMIT = 10
ARGS_DEFAULT_STATUS = ['READY', 'TASKED', 'DONE']

SUPERVISOR_ENABLED = False
SUPERVISOR_DEBUG = True
SUPERVISOR_POLITE = 3
#################################
# Background -- Celery
#################################
CELERY_WORKERS = 8
CELERY_MODULE = 'background'
# CELERY_BROKER = 'amqp://michael:michael123@localhost/michael_vhost'
CELERY_BROKER = 'amqp://{}:{}@{}/{}'.format(_celery_broker_uname, _celery_broker_pword, _celery_broker_host, _celery_broker_virtual_host)
CELERY_BACKEND = 'rpc://'
CELERY_INCLUDE = ['artifice.scraper.background.tasks']

CELERY_LOG_LEVEL = 'ERROR'
CELERY_LOG_FILE = 'celery.log'

URL_FOR_STATUS = 'http://{}:{}/status'.format(_eth0, _exposed_port)
URL_FOR_QUEUE = 'http://{}:{}/queue'.format(_eth0, _exposed_port)
URL_FOR_CONTENT = 'http://{}:{}/content'.format(_eth0, _exposed_port)
