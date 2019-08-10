from functools import wraps
from flask import make_response, jsonify, request


def reply_success(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 200)


def reply_error(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 422)


# @requires_body
def requires_body(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.data:
            return f(*args, **kwargs)
        else:
            return reply_error(error='Request body cannot be empty')
    return wrap


def url_value_is_list(data):
    return isinstance(data.get('url'), list)


def url_list_to_many(data):
    reply = []
    for url in data.get('url'):
        reply.append(dict(url=url))
    return reply
