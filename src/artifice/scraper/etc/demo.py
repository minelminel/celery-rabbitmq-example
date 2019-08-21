import marshmallow as ma
from marshmallow import fields, pprint

class UrlSchema(ma.Schema):
    url = fields.URL(required=True)
    msg = fields.Str()

schema = UrlSchema()

stuff = dict(
    url='https://www.npr.org/sections/politics/',
    msg='hello world',
)

data, errors = schema.load(stuff)
pprint(data)
pprint(errors)

data, errors = schema.dump(stuff)
pprint(data)
pprint(errors)
