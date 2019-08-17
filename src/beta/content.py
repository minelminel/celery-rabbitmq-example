'''
content.json contains a representation of a typical request body that would be sent to the /content [POST] endpoint.

load()
    • Convert any list values to a '|' delimited string on load
dump()
    • Convert the string to a list by splitting at our delimiter

'''
import os
import json
import marshmallow as ma
from marshmallow import fields, pprint, pre_load, pre_dump, post_dump

def render(result):
    if result.errors:
        print('[ERRORS]')
        pprint(result.errors)
    elif result.data:
        print('[DATA]')
        pprint(result.data)

def load_example():
    loc = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(loc, 'content.json')) as f:
        json_data = json.load(f)
    return json_data

content = load_example()
# pprint(content)

class ContentSchema(ma.Schema):
    origin = fields.Str(required=True)
    title = fields.Str(required=True)
    text = fields.Str(required=True)
    captions = fields.Str(required=True)
    url = fields.Str(required=True)

    @pre_load
    def list_to_string(self, data):
        convert = ['url','captions']
        for each in convert:
            value = data.get(each)
            joined = '|*|'.join(value)
            data[each] = joined
        return data


content_schema = ContentSchema()

load_result = content_schema.load(content)
# render(load_result)
# print('-'*50)
dump_result = content_schema.dump(load_result.data)
# render(dump_result)


class StringList(ma.fields.Field):
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


class TestSchema(ma.Schema):
    age = fields.Integer()
    colors = StringList()

test_schema = TestSchema()

stuff = dict(name='michael', age=25, colors=['blue', 'green', 'yellow'])
result = test_schema.load(stuff)
# render(result)
result = test_schema.dump(result.data)
# render(result)


# #
# SIDE LOADING
# #
'''
# input
{
    "color":["red","green","blue"]
}

# output
[
    {"color":"red"},
    {"color":"green"},
    {"color":"blue"},
]
'''

ex_ideal = dict(
    color=["red","green","blue"]
)

def side_load(data):
    reply = []
    for key, val in data.items():
        if isinstance(val, list):
            for each in val:
                reply.append({key:each})
        else:
            reply.append({key:val})
    return reply


print(f'[ideal]\n{side_load(ex_ideal)}\n','--'*50)

# class SideSchema(ma.Schema):
#     color = fields.Nested("self", many=True)
#
#     @post_dump
#     def foo(self, data):
#         print(data)
#
# side_schema = SideSchema()
#
# before = dict(
#     color=["red","green","blue"]
# )
# pprint(before)
#
# result = side_schema.dump(before)
# render(result)
