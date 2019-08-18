from celery import Celery

celery_app = Celery(
    'background',
    broker='amqp://michael:michael123@localhost/michael_vhost',
    backend='rpc://',
    include=['artifice.scraper.background.tasks'],
)
