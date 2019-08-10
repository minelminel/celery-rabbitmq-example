import os
import datetime
from pprint import pprint
from functools import wraps
from flask_restful import Resource
from flask import request, redirect, jsonify
from sqlalchemy.exc import IntegrityError

##### PROJECT IMPORTS #####

from . import app, api, db, ma
from .supervisor import Supervisor
from .models import Queue
from .schemas import QueueSchema, StatusSchema, ContentSchema
from .utils import reply_success, reply_error, requires_body, url_value_is_list, url_list_to_many

from test_celery import holding_tank

##### OBJECTS #####

supervisor = Supervisor(enabled=True)
status_schema = StatusSchema()
queue_schema = QueueSchema()
queues_schema = QueueSchema(many=True)
content_schema = ContentSchema()

##### API #####
def handle_url_list_case(json_data):
    if url_value_is_list(json_data):
        data, errors = queues_schema.load(url_list_to_many(json_data))
    else:
        data, errors = queue_schema.load(json_data)
        data = [data]
    return data, errors


class Api_Status(Resource):

    def get(self):
        return jsonify(supervisor.status())

    @requires_body
    def post(self):
        arg = request.get_json().get('enabled')
        data, errors = status_schema.load(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            supervisor.toggle_status(data)
            return reply_success(supervisor.status())


class Api_Queue(Resource):
    # return all url database entries
    def get(self):
        urls = db.session.query(Queue).all()
        result = queues_schema.dump(urls)
        return reply_success(result)

    # called from celery when enabled=False
    @requires_body
    def put(self):
        data, errors = handle_url_list_case(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            reply = []
            for each in data:
                url = each['url']
                result = db.session.query(Queue).filter_by(url=url).first()
                if result:
                    result.tombstone = False
                    db.session.commit()
                    data, errors = queue_schema.dump(result)
                    reply.append(dict(data=data, errors=errors))
                else:
                    q = Queue(url=url)
                    db.session.add(q)
                    db.session.commit()
                    data, errors = queue_schema.dump(db.session.query(Queue).filter_by(id=q.id).first())
                    reply.append(dict(data=data, errors=errors))
            return reply_success(reply)

    # add directly to celery task, no db entry
    @requires_body
    def post(self):
        data, errors = handle_url_list_case(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            # TODO: eliminate previously visited urls
            # tip: if all urls are removed from the list, this loop will be skipped without errors being raised and a 200 returned.
            for each in data:
                url = each['url']
                holding_tank.delay(url)
            return reply_success(data)


class Api_Content(Resource):

    def get(self):
        return reply_success()

    @requires_body
    def post(self):
        json_data = request.get_json()
        data, errors = content_schema.dump(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            reply = []
            urls = url_list_to_many(data)
            data, errors = queues_schema.load(urls)
            for each in data:
                # * * *
                # THIS SHOULD BE THE CONTENT DATABASE WHERE THIS INFO IS BEING STORED, RIGHT NOW ITS JUST A REPEAT OF THE OTHER METHODS
                # * * *
                q = Queue(url=each['url'])
                db.session.add(q)
                db.session.commit()
                data, errors = queue_schema.dump(db.session.query(Queue).filter_by(id=q.id).first())
                reply.append(dict(data=data, errors=errors))
            return reply_success(reply)


api.add_resource(Api_Status, '/status')
api.add_resource(Api_Queue, '/queue')
api.add_resource(Api_Content, '/content')
