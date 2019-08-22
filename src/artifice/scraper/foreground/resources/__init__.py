import logging
from flask import Blueprint
from flask_restful import Api

# url_prefix from settings.cfg
v1 = Blueprint('v1', __name__)

api = Api()
api.init_app(v1)

from .redis import reset_redis_hits, increment_redis
from .index import Api_Index
from .stats import Api_Stats
from .status import Api_Status
from .queue import Api_Queue
from .content import Api_Content

api.add_resource(Api_Index,     '/')
api.add_resource(Api_Stats,     '/stats')
api.add_resource(Api_Status,    '/status')
api.add_resource(Api_Queue,     '/queue')
api.add_resource(Api_Content,   '/content')
