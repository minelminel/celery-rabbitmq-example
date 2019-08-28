from marshmallow import Schema, fields #, pre_dump

import artifice.scraper.config.settings as settings
from .custom import Uppercase


class ArgsSchema(Schema):
    limit = fields.Int(required=False, default=settings.ARGS_DEFAULT_LIMIT)


class QueueArgsSchema(ArgsSchema):
    status = fields.List(Uppercase(required=False), default=settings.ARGS_DEFAULT_STATUS)

    # @pre_dump
    # def spaces_to_native(self, data):
    #     key = 'status'
    #     value = data.get(key)
    #     if isinstance(value, list):
    #         after = value.pop().split(' ')
    #         data[key] = after
    #     return data
