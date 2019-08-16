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
    url = fields.Str(required=True)
    status = fields.Str(default='READY') #  'TASKED'  'DONE'


class QueueArgsSchema(ma.Schema):
    # TODO: fix the terrible load logic, super hack-y right now
    limit = fields.Int(required=False, default=10)
    status = fields.Str(required=False)

    @post_load
    def validate_and_verify(self, data):
        whitelist = ['READY','TASKED','DONE']
        status = data.get('status')
        if status:
            if not isinstance(status, list):
                status_list = status.split(',')
            else:
                status_list = status
            status_list = [s.upper().strip() for s in status_list]
            status_dict = dict.fromkeys(status_list)
            for key in status_list:
                if key not in whitelist:
                    status_dict.pop(key)
            data['status'] = list(status_dict.keys())
        else:
            data['status'] = whitelist
        if not data.get('limit'):
            data['limit'] = 10
        return data


class StatusSchema(ma.Schema):
    enabled = fields.Boolean(required=True)


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
