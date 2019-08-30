try:
    import configparser
except ImportError:
    configparser = None

import os
import logging

log = logging.getLogger(__name__)

loc = os.path.dirname(os.path.abspath(__file__))

class Settings(object):
    """
        The settings can be changed by setting up a config file.
        For an example of a config file, see
        `scraper.cfg` in the main-directory.
    """
    def __init__(self):
        """
            Sets the default values for the project
        """
        # BASE_DIR:///artifice/scraper/
        self.BASE_DIR = os.path.dirname(loc)

        # prototypes
        self._eth0 = '0.0.0.0'
        self._exposed_port = 8080
        self._db_name = 'site.db'
        self._redis_pword = 'password'
        self._redis_host = 'localhost'
        self._redis_port = 6379
        self._celery_broker_uname = 'michael'
        self._celery_broker_pword = 'michael123'
        self._celery_broker_host = 'localhost'
        self._celery_broker_virtual_host = 'michael_vhost'

        # flask
        self.TESTING = False
        self.URL_PREFIX = ''
        self.FLASK_PORT = self._exposed_port
        self.FLASK_HOST = '0.0.0.0'
        self.FLASK_DEBUG = False
        self.FLASK_USE_RELOADER = False
        self.FLASK_THREADED = True

        # logging
        self.LOG_FILE = 'flask.log'
        self.LOG_LEVEL = 'INFO'
        self.CELERY_LOG_LEVEL = 'ERROR'
        self.CELERY_LOG_FILE = 'celery.log'
        self.STDOUT = True

        # database
        self.DROP_TABLES = True
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(
                                        os.path.join(self.BASE_DIR, self._db_name))

        # redis
        self.REDIS_URL = 'redis://{}:@{}:{}/0'.format(
                                        self._redis_pword,
                                        self._redis_host,
                                        self._redis_port)
        self.REDIS_HIT_COUNTER = 'HIT_COUNTER'

        # defaults
        self.ARGS_DEFAULT_LIMIT = 10
        self.ARGS_DEFAULT_STATUS = ['READY', 'TASKED', 'DONE']

        self.SUPERVISOR_ENABLED = True
        self.SUPERVISOR_DEBUG = False
        self.SUPERVISOR_POLITE = 1

        # celery
        self.CELERY_WORKERS = 8
        self.CELERY_MODULE = 'background'
        self.CELERY_BROKER = 'amqp://{}:{}@{}/{}'.format(
                                        self._celery_broker_uname,
                                        self._celery_broker_pword,
                                        self._celery_broker_host,
                                        self._celery_broker_virtual_host)
        self.CELERY_BACKEND = 'rpc://'
        self.CELERY_INCLUDE = ['artifice.scraper.background.tasks']

        # endpoints
        self.URL_FOR_STATUS = 'http://{}:{}/status'.format(self._eth0, self._exposed_port)
        self.URL_FOR_QUEUE = 'http://{}:{}/queue'.format(self._eth0, self._exposed_port)
        self.URL_FOR_CONTENT = 'http://{}:{}/content'.format(self._eth0, self._exposed_port)


    def init_from(self, file=None, envvar=None, log_verbose=False):
        if envvar:
            file = os.getenv(envvar)
            if log_verbose:
                log.info("Running with config from: " + (str(file)))

        if not file:
            return

        try:
            parser = configparser.RawConfigParser()
            parser.read(file)

            # parse prototypes
            # parse flask
            # parse logging
            # parse database
            # parse redis
            # parse defaults
            # parse celery
            # parse endpoints
        except AttributeError:
            log.info("Cannot use configparser in Python2.7")
            raise
