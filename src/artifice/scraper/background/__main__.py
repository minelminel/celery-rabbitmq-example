from . import celery_app

celery_app.start(argv=['celery', 'worker', '--loglevel','INFO','--logfile', 'celery.log'])
