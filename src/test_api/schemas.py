import os
from marshmallow import fields, ValidationError, post_load, pre_load, post_dump

from . import ma
from .models import Content, Queue

# ma.validator
def must_not_be_blank(data):
    if not data:
        raise ValidationError('Data not provided.')


class QueueSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    url = fields.Str(required=True, validate=must_not_be_blank)
    tombstone = fields.Boolean()


class StatusSchema(ma.Schema):
    enabled = fields.Boolean(required=True, validate=must_not_be_blank)


class ContentSchema(ma.Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
    origin = fields.Str(required=True, validate=must_not_be_blank)
    title = fields.Str()
    text = fields.Str()
    captions = fields.Str()

    @pre_load
    def join_captions(self, data, **kwargs):
        data['captions'] = '|'.join(data['captions'])
        return data

    @post_dump
    def split_captions(self, data, **kwargs):
        data['captions'] = data['captions'].split('|')
        return data
