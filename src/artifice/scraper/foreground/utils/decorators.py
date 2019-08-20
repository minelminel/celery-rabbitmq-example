from functools import wraps

from .replies import reply_error

# @requires_body
def requires_body(f):
    from flask import request
    @wraps(f)
    def wrap(*args, **kwargs):
        if request.data:
            return f(*args, **kwargs)
        else:
            return reply_error(error='Request body cannot be empty')
    return wrap
