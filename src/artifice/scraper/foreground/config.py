import os
import sys
import logging

loc = os.path.dirname(os.path.abspath(__file__))

class Config:
    # database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(loc, 'site.db'))
    # redis
    REDIS_URL = 'redis://password:@localhost:6379/0'
    REDIS_HIT_COUNTER = 'HIT_COUNTER'
    # flask development
    FLASK_PORT = 8080
    FLASK_HOST = '0.0.0.0'
    FLASK_DEBUG = True
    FLASK_USE_RELOADER = False
    # reset db at startup
    DROP_TABLES = True
    # logging
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'flask.log'
    STDOUT = True
    # supervisor
    SUPERVISOR_ENABLED = True
    SUPERVISOR_DEBUG = False


def configure_logger(configuration):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handlers = []

    if configuration.LOG_FILE is not None:
        file_handler = logging.FileHandler(filename=configuration.LOG_FILE, mode='a')
        file_handler.setFormatter(formatter)
        handlers.append(file_handler)
    if configuration.STDOUT is True:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setFormatter(formatter)
        handlers.append(stream_handler)

    logging.basicConfig(
        datefmt='%m/%d/%Y %I:%M:%S %p',
        level=getattr(logging, configuration.LOG_LEVEL),
        handlers=handlers
    )
