import logging
from flask import request
from flask_restful import Resource

from ..models import db, Queue, Content
from ..utils import reply_success, requests_per_minute
from ..supervisor import supervisor
from .redis import get_redis_hits

log = logging.getLogger(__name__)


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
