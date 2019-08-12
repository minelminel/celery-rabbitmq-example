from .tasks import holding_tank
from .celery import celery_app
# to start Celery in a terminal:
# celery -A test_celery worker --loglevel=info
