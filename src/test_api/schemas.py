import os
from marshmallow import fields, ValidationError, post_load, pre_load, post_dump

from . import ma
from .models import Content, Queue

# ma.validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data must not be blank.')


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

    @post_dump
    def remove_slash(self, data):
        key = 'url'
        value = data.get(key)
        if value:
            data[key] = value.strip('/')
        return data


class ArgsSchema(ma.Schema):
    limit = fields.Int(required=False, default=10)


class QueueArgsSchema(ArgsSchema):
    status = fields.List(Uppercase(required=False), default=['READY','TASKED','DONE'])


class StatusSchema(ma.Schema):
    enabled = fields.Boolean(required=False)
    debug = fields.Boolean(required=False)
    politeness = fields.Number(required=False)

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
