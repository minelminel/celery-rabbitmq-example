# Resource args_schema request db reply_success reply_error content_schema reply_auto contents_schema IntegrityError log
import logging
from flask import request
from sqlalchemy.exc import IntegrityError
from flask_restful import Resource

from ..models import db, Content
from ..utils import reply_success, reply_error, reply_auto, requires_body
from ..schemas import content_schema, contents_schema, args_schema

log = logging.getLogger(__name__)


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
