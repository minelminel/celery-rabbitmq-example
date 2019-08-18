import os
import logging
import datetime
from functools import wraps
from operator import attrgetter
import flask
from flask_restful import Resource
from flask import request, redirect, jsonify
from sqlalchemy.exc import IntegrityError
##### PROJECT IMPORTS #####
from . import app, api, db, ma, redis_client
from .supervisor import Supervisor
from .models import Queue, Content
from .schemas import QueueSchema, StatusSchema, ContentSchema, ArgsSchema, QueueArgsSchema
from .utils import reply_success, reply_error, reply_conflict, reply_auto, requires_body, side_load, requests_per_minute
##### ADJACENT IMPORTS #####
from artifice.scraper.background import holding_tank

log = logging.getLogger(__name__)

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

##### REDIS #####
def increment_redis():
    key = app.config['REDIS_HIT_COUNTER']
    try:
        redis_client.incr(key)
    except redis.exceptions.ConnectionError as e:
        log.error(f'[INCREMENT HITS] {str(e)}')

def get_redis_hits():
    key = app.config['REDIS_HIT_COUNTER']
    try:
        hits = int(redis_client.get(key))
    except redis.exceptions.ConnectionError as e:
        log.error(f'[BEFORE FIRST REQUEST] {str(e)}')
        hits = None
    return hits

def reset_redis_hits():
    key = app.config['REDIS_HIT_COUNTER']
    try:
        redis_client.set(key, 0)
    except redis.exceptions.ConnectionError as e:
        log.error(f'[RESET REDIS HITS] {str(e)}')

@app.before_first_request
def do_before_first_request():
    reset_redis_hits()

@app.before_request
def do_before_request():
    increment_redis()


##### API #####

class Api_Index(Resource):
    @staticmethod
    def routes_command(sort='endpoint', all_methods=False):
        """Show all registered routes with endpoints and methods.
            modified from the terminal print method in flask.cli  """
        reply = []
        rules = list(app.url_map.iter_rules())
        if not rules:
            return reply
        ignored_methods = set(() if all_methods else ("HEAD", "OPTIONS"))
        if sort in ("endpoint", "rule"):
            rules = sorted(rules, key=attrgetter(sort))
        elif sort == "methods":
            rules = sorted(rules, key=lambda rule: sorted(rule.methods))
        rule_methods = [",".join(sorted(rule.methods - ignored_methods)) for rule in rules]
        for rule, methods in zip(rules, rule_methods):
            if rule.endpoint != 'static':
                reply.append(dict(endpoint=rule.endpoint,methods=methods.split(','),rule=rule.rule))
        return reply


    def get(self):
        routes = self.routes_command()
        return reply_success(routes)


class Api_Stats(Resource):
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
        queue = self.queue_statistics()
        content = self.content_statistics()
        database = dict(Queue=queue,Content=content)
        uptime = supervisor.uptime()
        total_requests = get_redis_hits()
        rpm = requests_per_minute(uptime, total_requests)
        service = dict(uptime=uptime,requests=total_requests,rpm=rpm)
        return reply_success(database=database,service=service)


class Api_Status(Resource):
    # view whether status is enabled
    def get(self):
        msg = 'hello world'
        return reply_success(msg=msg, **supervisor.status())

    # turn the service on & off
    @requires_body
    def post(self):
        data, errors = status_schema.load(request.get_json())
        if errors:
            log.error({__class__:errors})
            return reply_error(errors)
        elif data:
            changed = supervisor.toggle_status(data)
            log.info(f'[changed] {changed}')
            msg = supervisor.render_msg(changed)
            # return self.put() # calls PUT method directly to release urls
        return reply_success(msg=msg, **supervisor.status())

    # release all READY urls to the task queue
    def put(self):
        result = db.session.query(Queue).filter_by(status='READY').all()
        for r in result:
            r.status = 'TASKED'
            if not supervisor.status().get('debug'):
                holding_tank.delay(r.url)
            else:
                log.debug(f'[**debug**][STARTUP] {r.url}')
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
            log.error({__class__:errors})
            return reply_error(errors)
        elif data:
            reply = []
            for each in data:
                result = db.session.query(Queue).filter_by(url=each.url).first()
                if result:
                    log.debug(f'[ALREADY IN QUEUE] {each.url}')
                    pass
                else:
                    log.debug(f'[ADDED TO QUEUE] {each.url}')
                    try:
                        db.session.add(each)
                        db.session.commit()
                        reply.append(queue_task_schema.dump(each).data)
                    except IntegrityError as e:
                        db.session.rollback()
                        log.error(data=each,error=str(e))
            for each in reply:
                if not supervisor.status().get('debug'):
                    holding_tank.delay(each.get('url'))
                else:
                    log.info(f'[**debug**][HOLDING_TANK] {each}')
            return reply_success(reply)
        return reply_auto(data, errors)

    # saves urls to queue db, called only be celery
    @requires_body
    def put(self):
        data, errors = queue_schema.load(request.get_json())
        if errors:
            log.error({__class__:errors})
            return reply_error(errors)
        elif data:
            log.debug(f'[RETURNING] {queue_schema.dump(data)}')
            result = db.session.query(Queue).filter_by(url=data.url).first()
            if result:
                result.status = data.status
            else:
                log.error(f'[MISSING] {queue_schema.dump(data)}')
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
            log.error({__class__:errors})
            return reply_error(errors)
        try:
            db.session.add(data)
            db.session.commit()
        except IntegrityError as e:
            log.error({__class__:str(e)})
            db.session.rollback()
        data, errors = content_schema.dump(db.session.query(Content).filter_by(id=data.id).first())
        return reply_auto(data, errors)


api.add_resource(Api_Index,     '/')
api.add_resource(Api_Stats,     '/stats')
api.add_resource(Api_Status,    '/status')
api.add_resource(Api_Queue,     '/queue')
api.add_resource(Api_Content,   '/content')
