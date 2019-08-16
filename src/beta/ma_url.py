import marshmallow as ma
from marshmallow import fields, pprint

# LOAD:: json => object
# DUMP:: object => json

def render(result):
    if result.errors:
        print('[ERRORS]')
        pprint(result.errors)
    elif result.data:
        print('[DATA]')
        pprint(result.data)

# Goal 1: be able to go from a json object to schema representation

url_dict = dict(
    url='https://www.npr.org/sections/politics'
)

# define the schema for the object
class UrlSchema(ma.Schema):
    url = fields.Str()
    status = fields.Str()

# create a schema instance
url_schema = UrlSchema()

# load the dict using the schema
result = url_schema.load(url_dict)
# print the results (result.data, result.errors)
render(result)
