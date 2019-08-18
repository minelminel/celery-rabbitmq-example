import math
import datetime
from functools import wraps
from flask import make_response, jsonify, request


def reply_success(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 200)


def reply_error(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 422)


def reply_conflict(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 409)


def reply_auto(data, errors):
    if errors:
        return reply_error(errors)
    elif data:
        return reply_success(data)
    else:
        return reply_conflict()


def _side_load(data):
    reply = []
    for key, val in data.items():
        if isinstance(val, list):
            for each in val:
                reply.append({key:each})
        else:
            reply.append({key:val})
    return reply


def side_load(key, data):
    return _side_load({key:data.get(key)})


def requests_per_minute(uptime, hits):
    '''
    ARGS::
        uptime => "0:13:32" <str> (hr:min:sec)
        hits   => 7 <int>
    # NOTE: uptime 'hours' never roll over for days!

    RETURNS::
        rate <int>
    # whatever the rate is calculated to be, we want to
    #    round the value UP to the nearest integer.
    '''
    if not hits:
        return 'unavailable'
    h, m, s = [int(n) for n in uptime.split(':')]
    as_minutes = (h*60) + (m) + (s/60)
    if as_minutes < 1:
        as_minutes = 1
    rpm = math.ceil(hits/as_minutes)
    return rpm


# @requires_body
def requires_body(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.data:
            return f(*args, **kwargs)
        else:
            return reply_error(error='Request body cannot be empty')
    return wrap


def setattrs(obj, **kwargs):
    for k, v in kwargs.items():
        setattr(obj, k, v)
    return obj


def cmp_dict(before, after):
    reply = {}
    for key, val in after.items():
        if before.get(key) != val:
            reply.update({key:after.get(key)})
    return reply
