import os
import datetime
from pprint import pprint
from functools import wraps
from operator import attrgetter
from flask_restful import Resource
from flask import request, redirect, jsonify
from sqlalchemy.exc import IntegrityError
##### PROJECT IMPORTS #####
from . import app, api, db, ma
from .supervisor import Supervisor
from .models import Queue, Content
from .schemas import QueueSchema, StatusSchema, ContentSchema
from .utils import reply_success, reply_error, reply_auto, requires_body, url_value_is_list, url_list_to_many
##### ADJACENT IMPORTS #####
from test_celery import holding_tank

##### OBJECTS #####
supervisor           = Supervisor(enabled=True)
##### SCHEMA INIT #####
status_schema        = StatusSchema()
queue_schema         = QueueSchema()
queues_schema        = QueueSchema(many=True)
queue_task_schema   = QueueSchema(exclude=('created_at','modified_at'))
queues_task_schema   = QueueSchema(many=True, exclude=('created_at','modified_at'))
content_schema       = ContentSchema()
contents_schema      = ContentSchema(many=True)

##### API #####
def handle_url_list_case(json_data):
    if url_value_is_list(json_data):
        data, errors = queues_schema.load(url_list_to_many(json_data))
    else:
        data, errors = queue_schema.load(json_data)
        data = [data]
    return data, errors


class Api_Index(Resource):

    def routes_command(sort='endpoint', all_methods=False):
        """Show all registered routes with endpoints and methods."""
        rules = list(app.url_map.iter_rules())
        if not rules:
            print("No routes were registered.")
            return
        ignored_methods = set(() if all_methods else ("HEAD", "OPTIONS"))
        if sort in ("endpoint", "rule"):
            rules = sorted(rules, key=attrgetter(sort))
        elif sort == "methods":
            rules = sorted(rules, key=lambda rule: sorted(rule.methods))
        rule_methods = [",".join(sorted(rule.methods - ignored_methods)) for rule in rules]
        reply = []
        for rule, methods in zip(rules, rule_methods):
            if rule.endpoint != 'static':
                reply.append(dict(endpoint=rule.endpoint,methods=methods.split(','),rule=rule.rule))
        return reply

    def get(self):
        routes = self.routes_command()
        return reply_success(routes)


class Api_Status(Resource):
    # view whether status is enabled
    def get(self):
        return jsonify(supervisor.status())

    # turn the service on & off
    @requires_body
    def post(self):
        arg = request.get_json().get('enabled')
        data, errors = status_schema.load(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            supervisor.toggle_status(data)
            return reply_success(supervisor.status())

    # start service from standstill
    def put(self):
        # release all READY urls to the task queue from standstill
        result = db.session.query(Queue).filter_by(status='READY').all()
        print(result)
        data, errors = queues_task_schema.dump(result)
        if errors:
            return reply_error(errors)
        elif data:
            print(data)
            reply = []
            for each in data:
                res = db.session.query(Queue).filter_by(id=each['id']).first()
                res.status = 'TASKED'
                db.session.commit()
                reply.append(res)
            for rep in reply:
                daa, err = queue_task_schema.dump(rep)
                url = daa.get('url')
                holding_tank.delay(url)
            return reply_success()
        return reply_success()


class Api_Queue(Resource):
    # show all entries from database
    def get(self):
        result = db.session.query(Queue).all()
        data, errors = queues_schema.dump(result)
        if errors:
            return reply_errors(errors)
        elif data:
            return reply_success(data)

    # post url(s) directly to celery tasks queue
    @requires_body
    def post(self):
        '''
        This should be the only place with entry to the celery task queue. Incoming requests can be either single or a list of object.

        >> schema.load request  ==> .: data, errors
        1.  check if url exists in database, if it does then set the status='TASKED', else create new row
        2.  dump to schema, append data & errors to list reply
        '''
        data, errors = handle_url_list_case(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            # add to database, skipping if already present
            reply = []
            for each in data:
                url = each['url']
                result = db.session.query(Queue).filter_by(url=url).first()
                if result:
                    if result.status != 'READY':
                        pass
                    result.status = 'TASKED'
                    db.session.commit()
                    daa, err = queue_task_schema.dump(db.session.query(Queue).filter_by(id=result.id).first())
                    if daa:
                        reply.append(daa)
                else:
                    q = Queue(url=url,status='TASKED')
                    db.session.add(q)
                    db.session.commit()
                    daa, err = queue_task_schema.dump(db.session.query(Queue).filter_by(id=q.id).first())
                    if daa:
                        reply.append(daa)
            for each in reply:
                url = each['url']
                holding_tank.delay(url)
        return reply_success(reply)

    # saves urls to database (queue, NOT content database)
    @requires_body
    def put(self):
        data, errors = queue_schema.dump(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            url = data['url']
            result = db.session.query(Queue).filter_by(url=url).first()
            result.status = data['status']
            db.session.commit()
            data, errors = queue_schema.dump(result)
            return reply_auto(data, errors)


class Api_Content(Resource):

    def get(self):
        contents = db.session.query(Content).all()
        data, errors = contents_schema.dump(contents)
        return reply_success(data)

    @requires_body
    def post(self):
        data, errors = content_schema.load(request.get_json())
        if errors:
            return reply_error(errors)
        elif data:
            try:
                c = Content(**data)
                db.session.add(c)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
            data, errors = content_schema.dump(db.session.query(Content).filter_by(id=c.id).first())
            return reply_auto(data, errors)


api.add_resource(Api_Index,     '/')
api.add_resource(Api_Status,    '/status')
api.add_resource(Api_Queue,     '/queue')
api.add_resource(Api_Content,   '/content')
