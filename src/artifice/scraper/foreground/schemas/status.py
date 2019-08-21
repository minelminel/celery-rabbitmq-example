from marshmallow import Schema, fields


class StatusSchema(Schema):
    enabled = fields.Boolean(required=False)
    debug = fields.Boolean(required=False)
    politeness = fields.Number(required=False)
