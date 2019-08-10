import os
from marshmallow import fields, ValidationError, pre_load

from . import ma

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
    enabled = fields.Boolean(required=True)

class ContentSchema(ma.Schema):
    url = fields.Str(dump_to='origin')
    links = fields.List(fields.Str(), dump_to='url')
    title = fields.Str()
    text = fields.Str()
    captions = fields.List(fields.Str())
