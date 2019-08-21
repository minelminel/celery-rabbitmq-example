from marshmallow import fields

from .. import ma


class StatusSchema(ma.Schema):
    enabled = fields.Boolean(required=False)
    debug = fields.Boolean(required=False)
    politeness = fields.Number(required=False)
