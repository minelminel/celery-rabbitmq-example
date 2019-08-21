# foreground/__init__.py
from flask import Flask
from flask_restful import Api
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import flask_monitoringdashboard as dashboard

from .config import Config, configure_logger

api = Api()
db = SQLAlchemy()
ma = Marshmallow()
redis_client = FlaskRedis()

# app = Flask(__name__)
# app.config.from_object(Config)
# api = Api(app)
# db = SQLAlchemy(app)
# ma = Marshmallow(app)
# redis_client = FlaskRedis(app)
# dashboard.bind(app)

def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)
    # with flask_app.app_context():
    #     init_db()
    api.init_app(flask_app)
    db.init_app(flask_app)
    ma.init_app(flask_app)
    redis_client.init_app(flask_app)

    # dashboard.bind(flask_app)
    from artifice.scraper.foreground.resources import v1
    flask_app.register_blueprint(v1, url_prefix='/v1')

    from .resources import reset_redis_hits, increment_redis

    @flask_app.before_first_request
    def do_before_first_request():
        reset_redis_hits()

    @flask_app.before_request
    def do_before_request():
        increment_redis()

    return flask_app
