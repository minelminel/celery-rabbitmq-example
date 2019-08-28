import logging
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource

from ..models import db, Queue
from ..utils import reply_success, reply_error, reply_auto, side_load, send_to_celery, requires_body
from ..schemas import queue_args_schema, queues_schema, queue_schema, queue_task_schema
from ..supervisor import supervisor

log = logging.getLogger(__name__)


class Api_Queue(Resource):
    # show all entries from database
    def get(self):
        params, _ = queue_args_schema.dump(request.args)
        result = db.session.query(Queue).filter(Queue.status.in_(params.get('status'))).limit(params.get('limit')).all()
        data, _ = queues_schema.dump(result)
        return reply_success(msg=params, reply=data)

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
                        log.error(data=each, error=str(e))
            for each in reply:
                if not supervisor.status().get('debug'):
                    # holding_tank.delay(each.get('url'))
                    send_to_celery(each.get('url'))
                else:
                    log.info(f'[**debug**][HOLDING_TANK] {each}')
            return reply_success(reply)
        return reply_auto(data, errors)

    # saves urls to queue db, used only by celery
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
