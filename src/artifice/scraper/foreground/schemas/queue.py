from marshmallow import fields

from ..models import Queue
from .base import BaseSchema
from .custom import SafeUrl, Uppercase


class QueueSchema(BaseSchema):
    class Meta:
        model = Queue
    url = SafeUrl(required=True)
    status = Uppercase(missing='TASKED', default='READY')
