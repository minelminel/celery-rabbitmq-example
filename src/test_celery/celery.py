from celery import Celery

celery_app = Celery(
    'test_celery',
    broker='amqp://michael:michael123@localhost/michael_vhost',
    backend='rpc://',
    include=['test_celery.tasks'],
)
