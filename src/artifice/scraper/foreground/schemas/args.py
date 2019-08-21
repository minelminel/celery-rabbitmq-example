from marshmallow import fields, pre_dump

from .. import ma
from .custom import Uppercase


class ArgsSchema(ma.Schema):
    limit = fields.Int(required=False, default=10)


class QueueArgsSchema(ArgsSchema):
    status = fields.List(Uppercase(required=False), default=['READY','TASKED','DONE'])

    @pre_dump
    def spaces_to_native(self, data):
        key = 'status'
        value = data.get(key)
        print(value, data)
        if isinstance(value, list):
            after = value.pop().split(' ')
            print(f'[after] {after}')
            data[key] = after
        return data
