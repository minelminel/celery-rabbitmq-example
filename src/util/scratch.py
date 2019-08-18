import sys
import inspect

def what_is_my_name():
    print(inspect.currentframe().f_code.co_name)
    # print(inspect.stack()[0][0].f_code.co_name)
    # print(inspect.stack()[0][3])
    print(sys._getframe().f_code.co_name)


# myself = lambda: inspect.stack()[1][3]
myself = lambda: inspect.stack()[1][3]

# myself()
#
# def foo(*args, **kwargs):
#     print('[ERROR] {}()'.format(myself()))
#
# foo()



def bar():
    print('inner')
    print(inspect.currentframe().__dict__)

def foo():
    print('outer')
    print(inspect.currentframe().__dict__)
    bar()

# foo()


before = dict(enabled=True,debug=False,politeness=1)

after = dict(enabled=True,debug=False,politeness=1.5)

# iterate thru keys, check corresponding value in other dict
# if values are different, append to reply
def cmp_dict(before, after):
    reply = {}
    for key, val in list(after.items()):
        if before.get(key) != val:
            reply.update({key:after.get(key)})
    return reply

r = cmp_dict(before, after)
print(r)
