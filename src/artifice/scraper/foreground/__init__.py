# foreground/__init__.py
import os
from flask import Flask, jsonify
from flask_restful import Api
from flask_redis import FlaskRedis
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import flask_monitoringdashboard as dashboard

from .config import Config


api = Api()
db = SQLAlchemy()
ma = Marshmallow()
redis_client = FlaskRedis()


def init_db(drop=False):
    from .models import db
    if drop:
        db.drop_all()
    db.create_all()


def create_app(*args, config_from=Config, **settings_override):
    # flask_app = Flask(__name__, instance_relative_config=True)
    flask_app = Flask(__name__)
    # load production/development config
    flask_app.config.from_object(config_from)
    # allow test config settings overrides
    flask_app.config.update(**settings_override)

    # # ensure the instance folder exists
    # try:
    #     os.makedirs(flask_app.instance_path)
    # except OSError:
    #     pass
    # raise ValueError(flask_app.config.get('SQLALCHEMY_DATABASE_URI'))

    redis_client.init_app(flask_app)
    api.init_app(flask_app)
    db.init_app(flask_app)
    ma.init_app(flask_app)

    ctx = flask_app.app_context()
    with ctx:
        init_db(drop=True)
    ctx.push()

    # dashboard.bind(flask_app)
    from artifice.scraper.foreground.resources import v1
    flask_app.register_blueprint(v1)
    # flask_app.register_blueprint(v1, url_prefix='/v1')

    from .resources import reset_redis_hits, increment_redis

    @flask_app.before_first_request
    def do_before_first_request():
        reset_redis_hits()

    @flask_app.before_request
    def do_before_request():
        increment_redis()

    return flask_app
