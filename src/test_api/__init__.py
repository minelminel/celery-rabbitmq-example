import os
from flask import Flask
from flask_redis import FlaskRedis
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

# from .config import *

loc = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(loc, 'site.db'))
app.config['REDIS_URL'] = 'redis://password:@localhost:6379/0'
app.config['REDIS_HIT_COUNTER'] = 'HIT_COUNTER'
# app.config.from_object('config.ProductionConfig')
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)
redis_client = FlaskRedis(app)
