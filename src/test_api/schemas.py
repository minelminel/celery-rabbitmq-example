import os
from marshmallow import fields, ValidationError, post_load, pre_load

from . import ma
from .models import Content, Queue

# ma.validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


# custom field
class StringList(fields.Field):
    '''
    >>> dump('red|blue|green')

        ['red','blue','green']

    >>> load(['red','blue','green'])

        'red|blue|green'
    '''
    def _serialize(self, value, attr, obj):
        # DUMP
        if not value:
            return []
        return value.split('|~|')

    def _deserialize(self, value, attr, obj):
        # LOAD
        if not value:
            return ''
        return '|~|'.join(value)


# custom field
class Uppercase(fields.Field):
    def _serialize(self, value, attr, obj):
        # DUMP
        if not value:
            value = ''
        return value.upper()


class QueueSchema(ma.ModelSchema):
    class Meta:
        model = Queue
    # 'READY'  'TASKED'  'DONE'
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    url = fields.Str(required=True)
    status = Uppercase(missing='TASKED', default='READY')


class ArgsSchema(ma.Schema):
    limit = fields.Int(required=False, default=10)


class QueueArgsSchema(ArgsSchema):
    status = fields.List(Uppercase(required=False), default=['READY','TASKED','DONE'])


class StatusSchema(ma.Schema):
    enabled = fields.Boolean(required=True)


class ContentSchema(ma.ModelSchema):
    class Meta:
        model = Content

    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    origin = fields.Str(required=True)
    title = fields.Str()
    text = fields.Str()
    captions = StringList()


# DEPRECATED -- QueueArgsSchema
# @post_load  # suuuuper janky
# def validate_and_verify(self, data):
#     whitelist = ['READY','TASKED','DONE']
#     status = data.get('status')
#     if status:
#         if not isinstance(status, list):
#             status_list = status.split(',')
#         else:
#             status_list = status
#         status_list = [s.upper().strip() for s in status_list]
#         status_dict = dict.fromkeys(status_list)
#         for key in status_list:
#             if key not in whitelist:
#                 status_dict.pop(key)
#         data['status'] = list(status_dict.keys())
#     else:
#         data['status'] = whitelist
#     if not data.get('limit'):
#         data['limit'] = 10
#     return data
