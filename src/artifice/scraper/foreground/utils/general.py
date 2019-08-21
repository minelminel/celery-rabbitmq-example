
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
