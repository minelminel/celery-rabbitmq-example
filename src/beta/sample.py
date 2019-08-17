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
    # url='https://www.npr.org/sections/politics',
    # status='DONE',
)

# define the schema for the object
class UrlSchema(ma.Schema):
    url = fields.Str(required=True)
    status = fields.Str(default='READY')

# create a schema instance
url_schema = UrlSchema()

# load the dict using the schema
result = url_schema.load(url_dict)
# print the results (result.data, result.errors)
print('* load')
render(result)
# >> result.data
# {'url': 'https://www.npr.org/sections/politics'}

# dump the dict using the schema
result = url_schema.dump(url_dict)
# print the results (result.data, result.errors)
print('* dump')
render(result)
# >> result.data
# {'status': 'READY', 'url': 'https://www.npr.org/sections/politics'}

# DEFAULTS ONLY ADDED WHEN DUMPING, NOT LOADING!
