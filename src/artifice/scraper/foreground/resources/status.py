import logging
from flask import request
from flask_restful import Resource

from ..models import db, Queue
from ..utils import reply_success, reply_error, send_to_celery, requires_body
from ..supervisor import supervisor
from ..schemas import status_schema, queues_schema

log = logging.getLogger(__name__)


class Api_Status(Resource):
    # view whether status is enabled
    def get(self):
        msg = ['hello world']
        return reply_success(msg=msg, **supervisor.status())

    # turn the service on & off
    @requires_body
    def post(self):
        data, errors = status_schema.load(request.get_json())
        if errors:
            log.error({__class__: errors})
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
                # holding_tank.delay(r.url)
                send_to_celery(r.url)
            else:
                log.debug(f'[**debug**][STARTUP] {r.url}')
        db.session.commit()
        reply = queues_schema.dump(result).data
        msg = f'{len(reply)} items released to task queue'
        return reply_success(msg=msg, reply=reply)
