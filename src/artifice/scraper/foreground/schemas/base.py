from marshmallow import fields

from .. import ma

class BaseSchema(ma.ModelSchema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)
