from .tasks import holding_tank
from .celery import celery_app
# to start Celery in a terminal:
# celery -A background worker --loglevel=info
