from flask import make_response, jsonify

def reply_success(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 200)


def reply_error(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 422)


def reply_conflict(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 409)


def reply_empty(*args, **kwargs):
    return make_response(jsonify(*args, **kwargs), 400)


def reply_auto(data, errors):
    if errors:
        return reply_error(errors)
    elif data:
        return reply_success(data)
    else:
        return reply_empty()
