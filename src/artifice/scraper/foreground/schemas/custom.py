from marshmallow import fields


class StringList(fields.Field):
    '''
    # serialize
    >>> dump('red|blue|green')

        ['red','blue','green']

    # deserialize
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


class Uppercase(fields.Field):

    def _serialize(self, value, attr, obj):
        # DUMP
        if not value:
            value = ''
        return value.upper()


class SafeUrl(fields.Field):
    '''
    This is a safe way to filter urls. Inputs can assume
    to be sanitized on load. Otherwise identical urls that
    differ only by a trailing slash may otherwise be indexed
    as two different entries. This causes orhan tasks to propegate.
    '''
    def _serialize(self, value, attr, obj):
        # DUMP
        if not value:
            value = ''
        return value.strip('/')

    def _deserialize(self, value, attr, obj):
        # LOAD
        if not value:
            value = ''
        return value.strip('/')
