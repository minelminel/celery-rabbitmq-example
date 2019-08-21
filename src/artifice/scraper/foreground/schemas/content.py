from marshmallow import fields

from ..models import Content
from .base import BaseSchema
from .custom import SafeUrl, StringList


class ContentSchema(BaseSchema):
    class Meta:
        model = Content
    origin = SafeUrl(required=True)
    title = fields.Str(missing='',default='')
    text = fields.Str(missing='',default='')
    captions = StringList()
