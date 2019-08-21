from flask_marshmallow import Marshmallow

# ma = Marshmallow()

from .args import *
from .queue import *
from .status import *
from .content import *
from .content import *

status_schema        = StatusSchema()
queue_schema         = QueueSchema()
queues_schema        = QueueSchema(many=True)
queue_task_schema    = QueueSchema(only=('status','url'))
queues_task_schema   = QueueSchema(many=True, only=('status','url'))
content_schema       = ContentSchema()
contents_schema      = ContentSchema(many=True)
args_schema          = ArgsSchema()
queue_args_schema    = QueueArgsSchema()
