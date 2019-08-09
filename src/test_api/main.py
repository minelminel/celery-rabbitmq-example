import os
import datetime
from functools import wraps

from flask import Flask, request, jsonify, make_response
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import fields, ValidationError, pre_load
from sqlalchemy.exc import IntegrityError

# from config import Configuration
#
# Config = Configuration()

##### CONFIG #####

loc = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(os.path.join(loc, 'site.db'))
api = Api(app)
db = SQLAlchemy(app)
ma = Marshmallow(app)


class ActionState:
    def __init__(self, enabled=False):
        self.enabled = enabled

    def status(self):
        return dict(enabled=self.enabled)

    def _enable(self):
        if not self.enabled:
            self.enabled = True

    def _disable(self):
        if self.enabled:
            self.enabled = False

    def toggle_status(self, data):
        if data.get('enabled') is True:
            self._enable()
        elif data.get('enabled') is False:
            self._disable()


State = ActionState()

##### MODELS #####

class Queue(db.Model):
    id = db.Column(db.Integer, nullable=False, unique=True, primary_key=True)
    created_at = db.Column(db.DateTime(), nullable=False, default=datetime.datetime.utcnow())
    modified_at = db.Column(db.DateTime(),nullable=True, onupdate=datetime.datetime.utcnow())
    url = db.Column(db.String(500), nullable=False, unique=True)
    tombstone = db.Column(db.Boolean(), nullable=True, default=False)

# class Content(db.Model):

# ma.validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


##### SCHEMAS #####

class QueueSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    url = fields.Str(required=True, validate=must_not_be_blank)
    tombstone = fields.Boolean()

    # @pre_load
    # def ensure_protocol(self, data):
    #     url_raw = data.get('url')
    #     if 'http://' or 'https://' not in url_raw:
    #         data.update(url='https://{}'.format(url))
    #     return data

class StatusSchema(ma.Schema):
    enabled = fields.Boolean(required=True)


status_schema = StatusSchema()

queue_schema = QueueSchema()
queues_schema = QueueSchema(many=True)


##### API #####

def reply_success(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 200)


def reply_error(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 422)


# @requires_body
def requires_body(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.data:
            return f(*args, **kwargs)
        else:
            return reply_error(error='Request body cannot be empty')
    return wrap


def url_value_is_list(data):
    return isinstance(data.get('url'), list)


def url_list_to_many(data):
    reply = []
    for url in data.get('url'):
        reply.append(dict(url=url))
    return reply


##### ENDPOINTS #####

class Api_Index(Resource):

    def get(self):
        urls = db.session.query(Queue).all()
        result = queues_schema.dump(urls)
        return reply_success(result)

    @requires_body
    def post(self):
        if url_value_is_list(request.get_json()):
            app.logger.info('List of URLs provided')
            data, errors = queues_schema.load(url_list_to_many(request.get_json()))
        else:
            app.logger.info('Single URL provided')
            data, errors = queue_schema.load(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            if isinstance(data, list):
                reply = []
                for each in data:
                    url = each['url']
                    q = Queue(url=url)
                    try:
                        db.session.add(q)
                        db.session.commit()
                        data, errors = queue_schema.dump(db.session.query(Queue).filter_by(id=q.id).first())
                    except IntegrityError as e:
                        db.session.rollback()
                        data = url
                        errors = dict(error=str(e))
                    reply.append(dict(data=data, errors=errors))
                return reply_success(reply)
            else:
                url = data['url']
                q = Queue(url=url)
                try:
                    db.session.add(q)
                    db.session.commit()
                    data, errors = queue_schema.dump(db.session.query(Queue).filter_by(id=q.id).first())
                except IntegrityError as e:
                    data = url
                    errors = dict(error=str(e))
                return reply_success(errors=errors,data=data)


class Api_Status(Resource):

    def get(self):
        return jsonify(State.status())

    @requires_body
    def post(self):
        arg = request.get_json().get('enabled')
        data, errors = status_schema.load(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            State.toggle_status(data)
            return reply_success(State.status())


api.add_resource(Api_Index, '/')
api.add_resource(Api_Status, '/status')


if __name__ == '__main__':

    db.create_all()
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=True,
        use_reloader=True,
    )
