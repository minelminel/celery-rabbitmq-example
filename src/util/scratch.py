
def setattrs(obj, **kwargs):
    for k, v in kwargs.items():
        setattr(obj, k, v)
    return obj


class Person(object):
    name = 'Michael'


def to_dict(obj):
    reply = {}
    [reply.update({a:getattr(obj, a)}) for a in dir(obj) if '__' not in a]
    return reply


# p1 = Person()
# p2 = Person()
#
# setattr(p1, 'age', 25)
# print(to_dict(p1))
#
# setattrs(p2, hello='world', number=42, correct=True)
# print(to_dict(p2))

# import os
#
# loc = os.path.dirname(os.path.abspath(__file__))
# temp = os.path.join(loc, 'temp')
# try:
#     os.mkdir(temp)
# except FileExistsError:
#     pass
