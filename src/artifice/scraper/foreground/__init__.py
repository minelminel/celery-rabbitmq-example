# foreground/__init__.py
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

# def init_db():
#     # import all modules which register a db object
#     from .models import db
#     db.create_all()

def create_app(config_class=Config):
    flask_app = Flask(__name__)
    flask_app.config.from_object(Config)

    redis_client.init_app(flask_app)
    api.init_app(flask_app)
    db.init_app(flask_app)
    # with flask_app.app_context():
    #     init_db()
    flask_app.app_context().push()
    ma.init_app(flask_app)

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

    @flask_app.route('/')
    def homepage():
        return jsonify(version=1, endpoint='/v1')

    return flask_app
