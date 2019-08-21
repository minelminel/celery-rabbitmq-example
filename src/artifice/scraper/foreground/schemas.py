import os
from marshmallow import fields, ValidationError, post_load, pre_load, pre_dump, post_dump

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


# custom field
class SafeUrl(fields.Field):
    '''
    This is a safe way to filter urls. Inputs can assume
    to be sanitized on load. Otherwise identical urls that
    differ only by a trailing slash may otherwise be indexed
    as two different entries. This causes orhan tasks to propegate.
    '''
    def _serialize(self, value, attr, obj):
        # DUMP
        if not value:
            value = ''
        return value.strip('/')

    def _deserialize(self, value, attr, obj):
        # LOAD
        if not value:
            value = ''
        return value.strip('/')


class BaseSchema(ma.ModelSchema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)


class QueueSchema(BaseSchema):
    class Meta:
        model = Queue
    url = SafeUrl(required=True)
    status = Uppercase(missing='TASKED', default='READY')


class ContentSchema(BaseSchema):
    class Meta:
        model = Content
    origin = SafeUrl(required=True)
    title = fields.Str(missing='',default='')
    text = fields.Str(missing='',default='')
    captions = StringList()


class StatusSchema(ma.Schema):
    enabled = fields.Boolean(required=False)
    debug = fields.Boolean(required=False)
    politeness = fields.Number(required=False)


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
