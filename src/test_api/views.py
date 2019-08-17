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
from .schemas import QueueSchema, StatusSchema, ContentSchema, ArgsSchema, QueueArgsSchema
from .utils import reply_success, reply_error, reply_gone, reply_auto, requires_body, url_value_is_list, url_list_to_many, side_load
##### ADJACENT IMPORTS #####
from test_celery import holding_tank

##### OBJECTS #####
supervisor           = Supervisor(enabled=True, debug=False)
##### SCHEMA INIT #####
status_schema        = StatusSchema()
queue_schema         = QueueSchema()
queues_schema        = QueueSchema(many=True)
queue_task_schema    = QueueSchema(only=('status','url'))
queues_task_schema   = QueueSchema(many=True, exclude=('created_at','modified_at'))
content_schema       = ContentSchema()
contents_schema      = ContentSchema(many=True)
args_schema          = ArgsSchema()
queue_args_schema    = QueueArgsSchema()

##### API #####

class Api_Index(Resource):
    @staticmethod
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

    @staticmethod
    def queue_statistics():
        return dict(
            total=db.session.query(Queue).count(),
            READY=db.session.query(Queue).filter_by(status='READY').count(),
            TASKED=db.session.query(Queue).filter_by(status='TASKED').count(),
            DONE=db.session.query(Queue).filter_by(status='DONE').count(),
        )

    @staticmethod
    def content_statistics():
        return dict(
            total=db.session.query(Content).count(),
        )

    def get(self):
        routes = self.routes_command()
        queue = self.queue_statistics()
        content = self.content_statistics()
        statistics = dict(queue=queue,content=content)
        return reply_success(api=routes,statistics=statistics)


class Api_Status(Resource):
    # view whether status is enabled
    def get(self):
        return reply_success(supervisor.status())

    # turn the service on & off
    @requires_body
    def post(self):
        data, errors = status_schema.load(request.get_json())
        if errors:
            app.logger.error({__class__:errors})
            return reply_error(errors)
        elif data:
            supervisor.toggle_status(data)
            # return self.put() # calls PUT method directly to release urls
        return reply_success(supervisor.status())

    # release all READY urls to the task queue
    def put(self):
        result = db.session.query(Queue).filter_by(status='READY').all()
        for r in result:
            r.status = 'TASKED'
            if not supervisor.status().get('debug'):
                holding_tank.delay(r.url)
            else:
                app.logger.info(f'[**debug STARTUP] {r.url}')
        db.session.commit()
        reply = queues_schema.dump(result).data
        msg = f'{len(reply)} items released to task queue'
        return reply_success(msg=msg,reply=reply)


class Api_Queue(Resource):
    # show all entries from database
    def get(self):
        params, _ = queue_args_schema.dump(request.args)
        result = db.session.query(Queue).filter(Queue.status.in_(params.get('status'))).limit(params.get('limit')).all()
        data, _ = queues_schema.dump(result)
        return reply_success(msg=params, response=data)

    # post url(s) directly to celery tasks queue
    @requires_body
    def post(self):
        json_data = side_load('url', request.get_json())
        data, errors = queues_schema.load(json_data)
        if errors:
            app.logger.error({__class__:errors})
            return reply_error(errors)
        elif data:
            reply = []
            for each in data:
                result = db.session.query(Queue).filter_by(url=each.url).first()
                if result:
                    app.logger.info(f'[ALREADY IN QUEUE] {each.url}')
                    pass
                else:
                    app.logger.info(f'[ADDED TO QUEUE] {each.url}')
                    db.session.add(each)
                    db.session.commit()
                    reply.append(queue_task_schema.dump(each).data)
            for each in reply:
                if not supervisor.status().get('debug'):
                    holding_tank.delay(each.get('url'))
                else:
                    app.logger.info(f'[**debug HOLDING_TANK] {each}')
            return reply_success(reply)
        return reply_auto(data, errors)

    # saves urls to queue db, called only be celery
    @requires_body
    def put(self):
        data, errors = queue_schema.load(request.get_json())
        if errors:
            app.logger.error({__class__:errors})
            return reply_error(errors)
        elif data:
            app.logger.info(f'[RETURNING] {queue_schema.dump(data)}')
            result = db.session.query(Queue).filter_by(url=data.url).first()
            if result:
                result.status = data.status
            else:
                app.logger.error(f'[MISSING] {queue_schema.dump(data)}')
                db.session.add(data)
            db.session.commit()
            data, _ = queue_schema.dump(result)
            return reply_success(data)


class Api_Content(Resource):
    # displays the stored content from db
    def get(self):
        params, _ = args_schema.dump(request.get_json())
        result = db.session.query(Content).limit(params['limit']).all()
        data, _ = contents_schema.dump(result)
        return reply_success(msg=params,reply=data)

    # stores gathered content to db
    @requires_body
    def post(self):
        data, errors = content_schema.load(request.get_json())
        if errors:
            app.logger.error({__class__:errors})
            return reply_error(errors)
        try:
            db.session.add(data)
            db.session.commit()
        except IntegrityError as e:
            app.logger.error({__class__:str(e)})
            db.session.rollback()
        data, errors = content_schema.dump(db.session.query(Content).filter_by(id=data.id).first())
        return reply_auto(data, errors)


api.add_resource(Api_Index,     '/')
api.add_resource(Api_Status,    '/status')
api.add_resource(Api_Queue,     '/queue')
api.add_resource(Api_Content,   '/content')
