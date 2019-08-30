from . import celery_app
from artifice.scraper.foreground import settings

celery_app.start(
    argv=[
        'celery',
        'worker',
        '--concurrency={}'.format(settings.CELERY_WORKERS),
        '--loglevel', settings.CELERY_LOG_LEVEL,
        '--logfile', settings.CELERY_LOG_FILE
    ]
)
