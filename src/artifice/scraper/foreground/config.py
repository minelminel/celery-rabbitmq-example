import os

loc = os.path.dirname(os.path.abspath(__file__))

class Config:
    # global
    TESTING = False
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
    SUPERVISOR_POLITE = 1
