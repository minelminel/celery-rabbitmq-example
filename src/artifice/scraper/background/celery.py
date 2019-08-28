from celery import Celery

import artifice.scraper.config.settings as settings

celery_app = Celery(
    settings.CELERY_MODULE,
    broker=settings.CELERY_BROKER,
    backend=settings.CELERY_BACKEND,
    include=settings.CELERY_INCLUDE,
)
